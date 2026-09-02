"""
Step 5: A comprehensive, general-purpose harness -- the FOSS shape of
Claude Code / Cursor / Copilot Agents.

Step 3 gave the model ONE narrow tool (place_box) for ONE domain. Step 4
gated a single generated script behind a human. Real coding agents
combine both ideas into an open-ended loop over a small, general tool
set that lets the model act directly on a filesystem and a shell:

    Claude Code tool   -->   here
    ---------------          ----------
    Read                     read_file
    Write                    write_file
    Edit                     edit_file      (unique old_string -> new_string)
    Bash                     bash
    TodoWrite                todo_write     (visible plan, not executed)
    (the human gate)         confirm()      -- asked before every write/edit/bash

Nothing here is domain-specific to boxes or COMPAS anymore. Give this
harness a different brief and it becomes a different agent. That is the
whole trick behind general-purpose coding agents: not a smarter loop,
but a *general enough* tool set plus the discipline to gate anything
that touches your disk or shell.

All file and shell activity is confined to ./workspace (created on first
run, gitignored). Read the "Safety note" near BASH_ONLY below before you
run this with --auto.

Run:
    python 05_mini_harness.py
    python 05_mini_harness.py "your own coding task"
    python 05_mini_harness.py --auto   (skip the human gate; for demos ONLY)
"""

import json
import subprocess
import sys
from pathlib import Path

from llm import MODEL, get_client

HERE = Path(__file__).parent
WORKSPACE = HERE / "workspace"
WORKSPACE.mkdir(exist_ok=True)

args = [a for a in sys.argv[1:] if a != "--auto"]
AUTO = "--auto" in sys.argv[1:]
TASK = args[0] if args else (
    "Create workspace/geometry_utils.py with a function box_volume(xsize, ysize, zsize) "
    "that returns the volume of a box, with a docstring. Then create "
    "workspace/test_geometry_utils.py with a few assert-based tests for it. "
    "Run the tests with bash. If anything fails, fix it and rerun until they pass."
)

# --- 1. The tools we hand to the model ----------------------------------
# General-purpose, not domain-specific: a real coding agent's tool set.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file from the workspace. Returns its contents.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a file in the workspace with the given content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": (
                "Replace one exact occurrence of old_string with new_string in a file. "
                "old_string must match the file's current content exactly and appear "
                "only once -- include surrounding lines for context if needed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "old_string": {"type": "string"},
                    "new_string": {"type": "string"},
                },
                "required": ["path", "old_string", "new_string"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List files and folders at a path inside the workspace (default: top level).",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run a shell command inside the workspace directory. Use it to run tests, scripts, etc.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "todo_write",
            "description": (
                "Replace the visible plan with this list of steps, so the human watching "
                "can follow along. Purely informational -- does not execute anything."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "todos": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string"},
                                "status": {
                                    "type": "string",
                                    "enum": ["pending", "in_progress", "completed"],
                                },
                            },
                            "required": ["content", "status"],
                        },
                    }
                },
                "required": ["todos"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": "Call this once the task is complete (or genuinely stuck).",
            "parameters": {
                "type": "object",
                "properties": {"summary": {"type": "string"}},
                "required": ["summary"],
            },
        },
    },
]

# --- 2. The tool implementations -----------------------------------------
# The harness owns real disk and shell access -- the model only ever
# *requests* an action by name; this code decides whether and how to run it.


def _resolve(path):
    """Keep file tools inside ./workspace. Never trust a model-supplied path."""
    target = (WORKSPACE / path).resolve()
    if target != WORKSPACE.resolve() and WORKSPACE.resolve() not in target.parents:
        raise ValueError(f"'{path}' escapes the workspace sandbox")
    return target


def read_file(path):
    target = _resolve(path)
    if not target.exists():
        return f"error: {path} does not exist"
    text = target.read_text()
    if len(text) > 4000:
        return text[:4000] + f"\n... [truncated, {len(text)} chars total]"
    return text or "(empty file)"


def write_file(path, content):
    target = _resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return f"ok, wrote {len(content)} chars to {path}"


def edit_file(path, old_string, new_string):
    target = _resolve(path)
    if not target.exists():
        return f"error: {path} does not exist -- use write_file to create it"
    text = target.read_text()
    count = text.count(old_string)
    if count == 0:
        return "error: old_string not found -- read_file again and copy it exactly"
    if count > 1:
        return f"error: old_string appears {count} times -- add more context to make it unique"
    target.write_text(text.replace(old_string, new_string, 1))
    return f"ok, edited {path}"


def list_dir(path="."):
    target = _resolve(path)
    if not target.exists():
        return f"error: {path} does not exist"
    entries = sorted(target.iterdir())
    if not entries:
        return "(empty directory)"
    return "\n".join(f"{'d' if e.is_dir() else 'f'}  {e.relative_to(WORKSPACE)}" for e in entries)


def bash(command):
    proc = subprocess.run(
        ["bash", "-c", command], cwd=WORKSPACE, capture_output=True, text=True, timeout=30
    )
    out = (proc.stdout + proc.stderr).strip()
    return f"exit code {proc.returncode}\n{out or '(no output)'}"


# --- Safety note ----------------------------------------------------------
# _resolve() keeps read_file/write_file/edit_file inside ./workspace. It
# CANNOT contain bash: a shell command can `cd ..`, use absolute paths, or
# call `rm`. This is exactly how Claude Code's real Bash tool works too --
# the sandbox is not the safety mechanism, the human reading each proposed
# command before approving it is. That is why every write_file, edit_file
# and bash call below is gated, and why --auto is for supervised demos only.
GATED_TOOLS = {"write_file", "edit_file", "bash"}
TOOL_FUNCS = {
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "list_dir": list_dir,
    "bash": bash,
    "todo_write": lambda todos: _todo_write(todos),
}

todos_state = []  # the harness keeps the plan around purely to print it


def _todo_write(todos):
    todos_state[:] = todos
    for t in todos:
        mark = "x" if t.get("status") == "completed" else (">" if t.get("status") == "in_progress" else " ")
        print(f"    [{mark}] {t.get('content', '')}")
    return f"ok, tracking {len(todos)} todo(s)"


def preview(name, a):
    """A short, human-readable description shown at the gate before approval."""
    if name == "write_file":
        content = a.get("content", "")
        snippet = content if len(content) <= 500 else content[:500] + "\n... [truncated]"
        return f"WRITE {a.get('path')}\n---\n{snippet}\n---"
    if name == "edit_file":
        return f"EDIT {a.get('path')}\n- {a.get('old_string')!r}\n+ {a.get('new_string')!r}"
    if name == "bash":
        return f"RUN (cwd=workspace): {a.get('command')}"
    return json.dumps(a)


def confirm(name, a):
    """THE HUMAN GATE. Same principle as 04, applied per tool call instead
    of per script: never let generated code, edits, or shell commands run
    unreviewed."""
    if AUTO:
        return True
    print(f"\n--- proposed action: {name} ---\n{preview(name, a)}\n" + "-" * 27)
    answer = input("Allow? [Enter = yes / n = deny] ")
    return not answer.strip().lower().startswith("n")


# --- 3. The conversation setup --------------------------------------------
messages = [
    {
        "role": "system",
        "content": (
            "You are a general-purpose coding agent working inside ./workspace. "
            "Use read_file/list_dir to look before you leap, write_file/edit_file to "
            "make changes, and bash to run and test what you wrote. Use todo_write "
            "to keep a short visible plan for multi-step tasks. Work in small, "
            "verifiable steps -- run the code you write and fix errors you find. "
            "Call finish with a one-line summary once the task is genuinely done."
        ),
    },
    {"role": "user", "content": TASK},
]

# --- 4. THE HARNESS: the same loop as step 3, over a general tool set -----
client = get_client()
MAX_STEPS = 30  # guardrail: this loop can run longer than 03's single-tool one

for step in range(MAX_STEPS):
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS, temperature=0, timeout=120
    )
    reply = response.choices[0].message

    if not reply.tool_calls:
        print(f"[step {step}] model said: {reply.content!r} -> nudging")
        messages.append({"role": "assistant", "content": reply.content})
        messages.append({"role": "user", "content": "Use the tools. Call finish when the task is done."})
        continue

    messages.append(
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in reply.tool_calls
            ],
        }
    )

    finished = False
    for tc in reply.tool_calls:
        name = tc.function.name
        try:
            a = json.loads(tc.function.arguments)
        except json.JSONDecodeError as e:
            result = f"error: bad JSON arguments ({e}). Retry with valid JSON."
            print(f"[step {step}] {name} FAILED -> {result}")
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
            continue

        if name == "finish":
            finished = True
            result = "task finished"
            print(f"[step {step}] finish: {a.get('summary', '')}")
        elif name not in TOOL_FUNCS:
            result = f"error: unknown tool {name}"
            print(f"[step {step}] {result}")
        elif name in GATED_TOOLS and not confirm(name, a):
            result = "error: human denied this action. Try a different approach, or ask via finish."
            print(f"[step {step}] {name} DENIED by human")
        else:
            try:
                result = TOOL_FUNCS[name](**a)
            except TypeError as e:
                result = f"error: bad arguments ({e})"
            except Exception as e:  # never let a bad tool call crash the harness
                result = f"error: {e}"
            print(f"[step {step}] {name}({a}) -> {result}")

        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    if finished:
        break
else:
    print(f"Stopped: budget of {MAX_STEPS} steps exhausted (guardrail).")

print(f"\nWorkspace: {WORKSPACE}")
print("Inspect what the model actually did:  ls workspace/  &&  cat workspace/<file>")
