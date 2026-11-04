"""
Step 4: A multi-agent workflow -- and where the HUMAN fits in.

Two "agents" collaborate here. Both are the same model; an agent's
"role" is nothing more than a different system prompt plus a different
position in the workflow:

    HUMAN (planner)  writes the brief, approves code before it runs,
                     judges the final result
    CODER agent      writes a complete COMPAS script
    HARNESS (code)   executes the script, catches crashes
    REVIEWER agent   checks the code against the brief, approves/rejects

    brief -> CODER -> [human gate] -> run it
                 ^                      |
                 |            crash? traceback goes back
                 |                      |
                 +---- REVIEWER <-- success: review code + output
                          |
                       approved -> done

Notice what was NOT automated: deciding WHAT to build, and whether the
result is actually good. That is your job now. The better your brief
and your judgment, the better this loop performs.

Run:
    uv run 04_coder_reviewer.py "an arch made of 15 boxes spanning 5 meters"
    uv run 04_coder_reviewer.py --auto   (skip the human gate; for demos)
    uv run view.py output/04_result.json
"""

import json
import re
import subprocess
import sys
from pathlib import Path

from llm import chat, get_client

HERE = Path(__file__).parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

args = [a for a in sys.argv[1:] if a != "--auto"]
AUTO = "--auto" in sys.argv[1:]
brief = args[0] if args else "an arch made of 15 boxes spanning 5 meters, 3 meters tall"

MAX_ROUNDS = 5  # guardrail

# --- The two roles: same model, different system prompts ----------------
# Small models write better code when we constrain the API surface to a
# short cheat-sheet instead of hoping they memorized the library.
CODER_SYSTEM = """You are a Python programmer writing COMPAS 2.x scripts.
Rules:
- Output exactly ONE python code block (```python ... ```), nothing else.
- Allowed imports: math, compas, compas.geometry.
- Build geometry with this API only:
    from compas.geometry import Box, Frame
    Frame([x, y, z], [1, 0, 0], [0, 1, 0])   # a frame at center point x,y,z
    Box(xsize, ysize, zsize, frame=frame)     # box centered on that frame
- Collect all geometry in a list called `result`.
- End the script with exactly:
    from compas import json_dump
    json_dump(result, "output/04_result.json")
    print(f"DONE: {len(result)} objects")
- Units are meters, z points up. A box resting on the ground has center z = zsize/2.
- Use clear variable names and brief comments: a human will review this code."""

REVIEWER_SYSTEM = """You are a strict code reviewer for an architecture-school
Python course. You receive a BRIEF, the CODE, and the OUTPUT of running it.
Check:
1. Does the code do what the brief asks (count, dimensions, arrangement)?
2. Is the geometry plausible (nothing floating, overlapping badly, or degenerate)?
3. Is the code readable (names, comments, no dead code)?
Reply with ONLY a JSON object, no markdown fences:
{"approved": true/false, "problems": ["..."], "advice": "one concrete instruction for the coder"}
Approve only if the brief is genuinely satisfied."""


def extract_code(text):
    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    return match.group(1) if match else None


def run_script(code):
    """Execute the generated script in a subprocess and capture the outcome."""
    script = HERE / "output" / "04_generated.py"
    script.write_text(code)
    proc = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True, text=True, timeout=60, cwd=HERE,
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


client = get_client()
coder_messages = [
    {"role": "system", "content": CODER_SYSTEM},
    {"role": "user", "content": f"Write the script for this brief: {brief}"},
]

for round_no in range(1, MAX_ROUNDS + 1):
    print(f"\n{'=' * 60}\nROUND {round_no}\n{'=' * 60}")

    # --- CODER writes (or rewrites) the script -------------------------
    reply = chat(client, coder_messages)
    coder_messages.append({"role": "assistant", "content": reply.content})
    code = extract_code(reply.content)
    if code is None:
        coder_messages.append(
            {"role": "user", "content": "You must output one ```python``` code block."}
        )
        continue
    print(code)

    # --- HUMAN GATE: never run unreviewed generated code automatically --
    # This is the single most important safety habit of agentic coding.
    if not AUTO:
        answer = input("\nRun this code? [Enter = yes / n = reject with a comment] ")
        if answer.strip().lower().startswith("n"):
            comment = input("Your feedback for the coder: ")
            coder_messages.append(
                {"role": "user", "content": f"Human reviewer rejected the code: {comment}"}
            )
            continue

    # --- HARNESS runs it and feeds errors back --------------------------
    returncode, output = run_script(code)
    print(f"\n--- execution ({'ok' if returncode == 0 else 'CRASHED'}) ---\n{output}")
    if returncode != 0:
        coder_messages.append(
            {"role": "user", "content": f"The script crashed:\n{output}\nFix it."}
        )
        continue

    # --- REVIEWER agent judges the result -------------------------------
    verdict_reply = chat(
        client,
        [
            {"role": "system", "content": REVIEWER_SYSTEM},
            {
                "role": "user",
                "content": f"BRIEF:\n{brief}\n\nCODE:\n{code}\n\nOUTPUT:\n{output}",
            },
        ],
    )
    match = re.search(r"\{.*\}", verdict_reply.content, re.DOTALL)
    verdict = json.loads(match.group(0)) if match else {"approved": False, "advice": "?"}
    print(f"\n--- reviewer ---\napproved: {verdict.get('approved')}")
    for p in verdict.get("problems", []):
        print(f"  problem: {p}")
    print(f"  advice: {verdict.get('advice', '')}")

    if verdict.get("approved"):
        print(f"\nAPPROVED after {round_no} round(s).")
        print("Final script: output/04_generated.py")
        print("View result:  python view.py output/04_result.json")
        break
    coder_messages.append(
        {
            "role": "user",
            "content": "Reviewer feedback: "
            + "; ".join(verdict.get("problems", []))
            + ". "
            + verdict.get("advice", ""),
        }
    )
else:
    print(f"\nStopped: {MAX_ROUNDS} rounds exhausted without approval (guardrail).")
    print("This happens with small models -- YOU are the senior reviewer: "
          "inspect output/04_generated.py and decide what is wrong.")
