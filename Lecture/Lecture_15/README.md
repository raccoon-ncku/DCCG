# Week 15 — Working with AI

> One session, three blocks:
>
> 1. **Build the loop** ([Part A](#part-a--build-the-loop), §1–3): the agent harness from scratch, on the
>    course model. *What an assistant actually is.*
> 2. **Put it in your pipeline** ([Part B](#part-b--put-it-in-your-pipeline)):
>    pytest as the reviewer that cannot be fooled, the human review that
>    remains, and day-to-day habits.
> 3. **Open block: one change, with an assistant.** On your own project: write
>    the test yourself, let an assistant write the function, open a pull
>    request, and have your Week 13 partner review it against the checklist.
>
> The [agentic lab](/Assignment/6_agentic_workflow/README.md) opens this week
> and is due in Week 17. §4–6 below are reading for the lab.

Here a language model writes the code, and you become the **planner** and the
**reviewer**. Building one of these tools from scratch shows you what it is, so you can
direct it with judgment.

> We use the course node's small model (`gemma-4-26b-4bit`, unlimited) on purpose: it
> fails often and visibly.

# Part A — Build the loop

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

Every agent framework is this loop with more engineering around it. Here it is about 40
lines of Python.

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
cp Lecture/Lecture_15/agents/.env.example Lecture/Lecture_15/agents/.env   # paste your class API key
```

Then `cd Lecture/Lecture_15/agents` and run the scripts with `uv run`, e.g.
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
Claude Code, Cursor and Copilot Agents work this way, with a stronger model and much
more engineering. Read the "Safety note" inside the file before using `--auto`.

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
4. In `05`, deny a `bash` call and give the model a comment explaining why. Does it
   find another way, or repeat the same call?
5. Compare `04` and `05`: one gates a whole script once, the other every disk and shell
   action. What does each buy you, and what does each cost in friction?

## 6. Outlook

[Part B](#part-b--put-it-in-your-pipeline) replaces
the reviewer agent with something that cannot be argued with: your test suite. MCP (Model
Context Protocol) is a standard for exposing tools to agents, for example driving Rhino
with `rhinomcp`.

---

# Part B — Put it in your pipeline

This part is about **handing an assistant one stage of the pipeline**.

| You built | So an assistant can be given | And cannot get past |
| --- | --- | --- |
| a spec as tests ([W10](/Lecture/Lecture_10/README.md#part-b--testing)) | "make these pass" instead of a paragraph | a red test |
| a review habit ([W13](/Lecture/Lecture_13/README.md)) | the job of author | you, reading the diff |
| a scaffold ([W09](/Lecture/Lecture_09/README.md#part-d--a-project-that-can-hold-components)) | one small pure module in `src/` | the folder structure: it has nowhere to hide logic |
| a verified build ([W14](/Lecture/Lecture_14/README.md)) | nothing: it runs by itself | the verifier |

## 7. pytest as the reviewer that cannot be fooled

```bash
uv run Lecture/Lecture_15/agents/tdd_agent.py
uv run Lecture/Lecture_15/agents/view.py Lecture/Lecture_13/output/wall.json
```

[`tdd_agent.py`](agents/tdd_agent.py) replaces the reviewer LLM of §3 with pytest: the
coder agent writes `wall.py`, the harness runs the tests, and failures go back
verbatim until green. An LLM reviewer can be argued into approving; a test suite
cannot. The raw `wall.py` it produces is the file you reviewed in [Week 13 §1](/Lecture/Lecture_13/README.md#1-correct-is-not-good): it
passes, and it is not good. **Both gates, always: the automatic one for correct,
the human one for good.**

## 8. The agentic development loop

Adding a new component to the plugin set:

```
1. SPEC     you write tests/test_canopy.py            ← the brief, human
2. CORE     agent writes src/compas_studio/canopy.py  ← delegated, but…
3. VERIFY   CI runs pytest on the PR                   ← the gate, automated
4. REVIEW   you read the diff: correct AND good?       ← judgment, human
5. ADAPTER  add components/Cs_Canopy/ (thin code.py)   ← you
6. SHIP     tag → ghuser-builder builds and verifies   ← automated
```

The human sits at the **ends** (what to build, whether it is good, what to ship)
and out of the **middle** (typing, running tests, packaging). The failure this
course is built to prevent is the opposite: a person in the middle, pasting what
the chatbot produced, unable to tell passing-but-bad from good.

## 9. Working with an assistant, day to day

- **Give it the test, not the wish.** "Make `tests/test_canopy.py` pass
  without changing the tests" is a task with an end. "Write a canopy
  generator" is a conversation.
- **One stage, one module.** Ask for a pure function in `src/`. Do not let
  one request touch the core, the adapter and the workflow together: you
  cannot review that diff.
- **It works on a branch.** Its changes arrive as a pull request you read,
  never as edits to `main`.
- **Read what it ran, not only what it wrote.** When a tool asks to execute
  a command, that is the human gate from §1. `--auto` is for demos.
- **Never let it edit the tests to make them pass.** If the test is wrong,
  that is your decision, made in a separate commit, with a reason.
- **Log what you asked.** The prompts that mattered go in `log.md`
  ([AI policy](/README.md#ai-usage)). At the oral defence you explain every
  line, whoever typed it.

## 10. Things to try in your pipeline

1. Add a fourth component end to end (a column grid, a vault). How many rounds
   did the agent need to pass your tests? Which failures were the model's, and
   which were your spec's?
2. Sabotage `Lecture_14/plugin_set/src/compas_studio/wall.py` (offset odd courses by a full
   module). Which test catches it?
3. Compare `Lecture_13/wall.py` with `Lecture_14/plugin_set/src/compas_studio/wall.py`. List five things
   a review catches and a test does not.
4. Break the adapter/metadata agreement: rename an input in `code.py` but not in
   `metadata.json`. Run `scripts/ghuser`, then `uv run pytest`. Which one stops it?

Optional: [trained models as design ingredients](neural/README.md).
