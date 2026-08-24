# Lecture 11: Agentic Workflows

Until now, *you* wrote every line of code. In this lecture we flip the roles:
a language model writes the code, and you move up one level — you become the
**planner** and the **reviewer**. This is how modern software teams
increasingly work with tools like Claude Code, Cursor, and Copilot Agents.

The goal is not to automate you away. It is to understand, by building one
from scratch, what these tools actually are — so you can direct them with
judgment instead of using them as magic.

> We deliberately use our course node's small model (`gemma-4-26b-4bit`,
> unlimited usage). It fails often, visibly, and instructively. Watching a
> small model fail teaches you more about agents than watching a frontier
> model succeed.

## 1. Concepts

### The LLM is a stateless function
An LLM maps a list of messages to one reply. It has no memory: the
"conversation" exists only because the caller re-sends the full history each
time. Whoever controls that message list controls the agent.

### Agent = LLM + tools + a loop
The model can only produce text. An **agent** emerges when a program — the
**harness** — gives the model tools (functions it may request), executes those
requests, feeds results back, and repeats until the task is done:

```
while not done:
    reply = model(messages, tools)
    if reply requests a tool:
        result = harness_runs_it()     # our code executes, never the model
        messages.append(result)        # the model sees what happened
    else:
        done
```

Every agent framework (CrewAI, LangGraph, Claude Code) is this loop with more
engineering around it. In this lecture you will read and modify the loop
itself — about 40 lines of Python.

### Multi-agent = multiple system prompts
A "coder agent" and a "reviewer agent" are the same model with different
system prompts, placed at different points of a workflow. The architecture of
the *workflow* (who talks to whom, who can veto) matters more than the model.

### What stays human
| Role | Who does it now |
|---|---|
| Writing the brief / spec | **You** (planner) |
| Typing the code | model |
| Running it safely | harness |
| First-pass critique | model (reviewer role) |
| Deciding "is this actually good?" | **You** (reviewer) |

The quality ceiling of the whole system is your brief and your judgment.

### Guardrails
Agents fail in loops, so a harness always has: a step budget (`MAX_STEPS`),
`temperature=0` (small quantized models hallucinate at higher temperatures),
defensive parsing (never trust model output), error *feedback* instead of
crashes, and a **human gate** before executing generated code.

## 2. Setup

```bash
cd DCCG                       # the folder with pyproject.toml / uv.lock
uv sync                       # openai is already a project dependency
cp Lecture/Lecture_11/.env.example Lecture/Lecture_11/.env   # paste your class API key
```

Then `cd Lecture/Lecture_11` and run the scripts with `uv run`, e.g.
`uv run 01_chat.py` — the commands below assume that working directory, and
`uv run` still finds the project environment from any subfolder.

Our node at `llm-api.rccn.dev` speaks the OpenAI protocol, so the standard
`openai` client works — only the `base_url` changes (see `llm.py`).

## 3. The five steps

Run them in order; each script's docstring explains one idea.

### `01_chat.py` — the LLM is just a function
One API call, no magic. Watch how "memory" is faked by re-sending history.

### `02_structured.py` — the LLM inside your program
The model outputs JSON, your code validates it and builds COMPAS geometry.
The model produces *data*, never touches your program directly.
```bash
uv run 02_structured.py "a spiral staircase of 12 steps, going up counter-clockwise"
uv run view.py output/02_boxes.json
```

### `03_agent_loop.py` — tools + loop = agent
The harness, hand-written. The model places boxes by calling a `place_box`
tool and sees each result. Watch the log: the model *will* produce malformed
calls — and correct itself when the harness reports the error back.
```bash
uv run 03_agent_loop.py "a bridge spanning 6 meters between two towers"
uv run view.py output/03_scene.json
```

### `04_coder_reviewer.py` — the multi-agent workflow, with you in it
A coder agent writes a full COMPAS script; you approve it before it runs
(the human gate); the harness executes it and feeds crashes back; a reviewer
agent checks the result against your brief and can send it back for rework.
```bash
uv run 04_coder_reviewer.py "an arch made of 15 boxes spanning 5 meters, 3 meters tall"
uv run view.py output/04_result.json
```
Try rejecting the code at the gate with your own feedback. Try a vague brief
versus a precise one and compare how many rounds each needs.

### `05_mini_harness.py` — a small, FOSS Claude Code
Step 3 gave the model one narrow tool for one domain (boxes). Step 4 gated
one generated script. This step combines both ideas into an open-ended
loop over a *general* tool set — read/write/edit files, run shell commands,
track a visible todo list — all confined to `./workspace` and gated by you
before anything touches disk or shell:
```bash
uv run 05_mini_harness.py
uv run 05_mini_harness.py "your own coding task, in plain English"
```
This is not a metaphor for how Claude Code, Cursor, or Copilot Agents work —
it *is* how they work, minus a decade of engineering (context compaction,
richer sandboxing, parallel tool calls, IDE integration, a much stronger
model). Read the "Safety note" inside the file before using `--auto`.

## 4. Safety note

`04_coder_reviewer.py` executes model-generated Python on your machine, and
`05_mini_harness.py` lets the model write files and run arbitrary shell
commands. That is why the human gate exists in both — **read code and
commands before you approve them**, always. The `--auto` flag (used for
classroom demos) is exactly the setting you should be suspicious of in real
tools.

## 5. Things to try

1. In `03`, raise the temperature to 1.0 and watch what happens to the agent.
2. In `03`, add a `remove_box(index)` tool. What else must change?
3. In `04`, make the reviewer stricter (e.g., demand a docstring and
   parametric variables). Does the loop still converge in 5 rounds?
4. Break it on purpose: ask for geometry the cheat-sheet API cannot express.
   Where does the failure show up — coder, harness, or reviewer?
5. In `05`, deny a `bash` call and give the model a comment explaining why.
   Does it find another way, or does it repeat the same call verbatim?
6. In `05`, add a `grep`-style search tool. Does the model start using
   `read_file` less and search more, the way you would?
7. Compare `04` and `05`: one gates a whole script once, the other gates
   every disk/shell action individually. What does each buy you, and what
   does each cost in friction?

## 6. Outlook

- **Next lecture**: the reviewer agent you met here can be wrong. Lecture 12
  replaces it with something that can't be argued with — a test suite — and
  shows how verified geometry ships into Rhino.
- **Frameworks**: what we hand-rolled here, packaged: CrewAI, LangGraph,
  the OpenAI Agents SDK. Same loop, more features.
- **MCP (Model Context Protocol)**: a standard for exposing tools to agents —
  e.g. driving Rhino directly from an agent (`rhinomcp`).
- **Agentic coding tools**: Claude Code, Cursor, Copilot Agents — a harness
  like `05`, with the file system, terminal, and git as tools, and a much
  stronger model. Your job when using them is the one you practiced today: plan,
  gate, review.
