# Week 01 — Toolchain: uv, Zed, git, and an AI assistant

> **Everything you need is in this repository.** There are no slides you must
> attend to understand this page, and no step that only works if someone shows
> you. If you get stuck, the fix is in here or in the error message.

## 0. What this week is for

By the end of today you will have a working Python environment, an editor, a
git identity, and an AI assistant — and you will have *proven* it by running
one command that checks all of it:

```bash
uv run check.py 01
```

That command is how every week in Part I and II works. Read §5 before you
start, so you know what you are aiming at.

## 1. Why this toolchain

We changed tools this semester. If you took a similar course before, or you
find an old tutorial online, you will see `conda` and VS Code. We now use:

| Job | Old | **Now** | Why |
| --- | --- | ------- | --- |
| Python + packages | conda | **uv** | One tool, ~10× faster, and it *locks* exact versions so your machine and mine agree |
| Editor | VS Code | **Zed** | Fast, and its AI integration shows you diffs to accept or reject — which is the reviewing habit this course is about |
| Version control | git | **git** | unchanged |

Nothing you learn is tool-specific: `uv` manages a normal Python virtual
environment, and Zed edits normal text files.

> **If you already have conda installed, leave it alone.** It will not
> conflict. Just do not use it for this course — mixing the two is the most
> common source of "it works for you but not for me".

## 2. Install

### 2.1 uv

macOS / Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Windows (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen your terminal, then confirm:
```bash
uv --version
```

### 2.2 git

macOS ships with git. Windows: install from <https://git-scm.com/downloads>.

Tell git who you are — this is what shows up on every commit you make all
semester, and one of this week's checkpoints looks for it:

```bash
git config --global user.name  "Your Name"
git config --global user.email "your@email.address"
```

### 2.3 Zed

Download from <https://zed.dev>. macOS and Linux are supported natively;
on Windows use the preview build, or stay on VS Code — **the editor is the one
tool here you may substitute.** Everything else in this repo assumes uv and git.

Useful Zed commands (`cmd`/`ctrl` + `shift` + `P` opens the palette):

| Action | Shortcut |
| ------ | -------- |
| Command palette | `cmd/ctrl + shift + P` |
| Open project | `cmd/ctrl + O` |
| Integrated terminal | `` ctrl + ` `` |
| Find in project | `cmd/ctrl + shift + F` |
| AI: inline assist | `ctrl + enter` |
| AI: chat panel | `cmd/ctrl + ?` |

### 2.4 An AI assistant

Pick **one** to start:

- **Zed's built-in assistant** — sign in with GitHub; free tier is enough.
- **GitHub Copilot** — free for students via the
  [GitHub Student Developer Pack](https://education.github.com/pack).
- **Claude Code / Codex CLI** — terminal-based agents. We use these properly in
  Weeks 11–14; you do not need one yet.

You will also get a key for the **course LLM node** (`llm-api.rccn.dev`) in
Week 11. It is free and unlimited for you, and deliberately runs a small model
that fails in visible, instructive ways.

## 3. Get the repository

```bash
git clone https://github.com/raccoon-ncku/DCCG.git DCCG
cd DCCG
uv sync
```

`uv sync` reads `pyproject.toml` and `uv.lock` and builds an exact,
reproducible environment in `.venv/`. It takes a minute the first time.

> **Week 01 is local-only.** You clone directly from the instructor's URL and
> commit A0 locally — no push required today. Next week we set up a
> **fork** so your commits land on your own copy, and the weekly `git pull`
> ritual for new course material begins. If you want to read ahead:
> [SETUP.md ▸ Git for this course](/SETUP.md#git-for-this-course) and
> [rccn wiki ▸ Git for coursework](https://kb.rccn.dev/computation/development-environment/version-control/coursework-git).
{.is-info}

### Your work vs. the instructor's

Two kinds of file live in this repo. The distinction matters for the rest of
the term:

| | Path | Whose | Rule |
| --- | --- | --- | --- |
| Instructor's | `Lecture/…/README.md`, `Reference/…` | theirs | you read, sometimes edit (checkpoint stubs) |
| Yours | [`MyWork/`](/MyWork/README.md) | yours | put notes, sketches, practice here |
| Private | `Notes/` | yours, laptop-only | gitignored — never pushed |

The instructor promises to never write into `MyWork/`, so `git pull` on Week 03
will never conflict with your Week 02 notes.

**You never activate this environment.** Instead, prefix commands with
`uv run`, which runs them inside it:

```bash
uv run python                       # a Python REPL with compas available
uv run Lecture/Lecture_01/Examples/1_hello_world.py
uv run check.py
```

If you *want* an activated shell (some editors like it), `source
.venv/bin/activate` still works — but `uv run` is the habit to build, because
it can never use the wrong Python by accident.

### Useful uv commands

| Command | What it does |
| ------- | ------------ |
| `uv sync` | Build/repair the environment to match the lockfile |
| `uv run <script.py>` | Run a script inside the environment |
| `uv add <package>` | Add a dependency (updates `pyproject.toml` + `uv.lock`) |
| `uv remove <package>` | Remove one |
| `uv tree` | Show what is installed and why |

## 4. Rhino (optional this week)

Rhino is not required until Week 14, but the licence is available now.

Download Rhino 8 from <https://www.rhino3d.com/download>. When prompted for a
licence, choose **`zoo`** as the authentication method and **`zoo.rccn.dev`**
as the server. It covers Rhino 6 and 8, Windows and Mac.

> The licence server is reachable only from the computer lab's wifi and from
> Workspace Raccoon.

Everything in this course runs **without** Rhino. That is the point of the
architecture you will meet in Week 06.

## 5. How checkpoints work

This repository is not a set of slides you read. Each week ships with
**checkpoints** — small, precisely-specified tasks — and a runner that tells
you whether you have them right.

```bash
uv run check.py        # overview of every week
uv run check.py 01     # this week, with hints
uv run check.py 01 -v  # ... and the full failure output
```

Each week's tasks live in `Lecture/<folder>/checkpoints/tasks.py`. You edit
**only that file**. Next to it, `test_tasks.py` is the *specification*: the
precise, machine-checkable statement of what your code must do. Read it. It is
allowed — in fact it is the point. A spec you are not allowed to read is not a
spec, it is a guessing game.

Three states:

| | meaning |
| - | ------- |
| `TODO` | not attempted yet — the stub still raises `NotImplementedError` |
| `FAIL` | attempted, but does not match the spec |
| `PASS` | correct |

**A `FAIL` is not a penalty — it is a fast, free, patient answer to "did I get
this right?".** Checkpoints aren't scored, but completing them is required (they
are your gate to the final project, which is the whole grade), so turning them
green is all that counts; run the checker as often as you like.

In Week 10 you will learn to *write* these specs yourself, and this runner
stops being magic.

### Using AI on checkpoints

Allowed, and encouraged. But the deal from the syllabus applies from day one:
**you must be able to explain every line you submit.** A checkpoint that passes
with code you cannot explain has taught you nothing and will cost you in Week
11, when your job becomes reviewing exactly this kind of code.

A good habit, starting now: try it yourself first, then ask the AI, then
*diff the two* and work out who was right and why.

## 6. This week's checkpoints

Open `Lecture/Lecture_00/checkpoints/tasks.py` and follow the instructions at
the top. Four of the five checks are diagnostics — they verify your install
rather than your code. The fifth asks you to edit one line.

```bash
uv run check.py 01
```

When all five pass, commit locally:

```bash
git add -A
git commit -m "Week 01: environment set up"
```

That commit is assignment **A0** — see
[A0: Setup & Copilot](/Assignment/0_copilot/README.md). No push this week; you
do not have a fork yet. Next week we set one up in the first ten minutes of
class and the commit above gets its first `git push`.

If you want to fork ahead of Week 02: the setup and the four weekly commands
are in [SETUP.md ▸ Git for this course](/SETUP.md#git-for-this-course).

## 7. Troubleshooting

**`uv: command not found`** — your terminal has not picked up the new PATH.
Close it and open a new one. If it persists, the installer prints the line to
add to your shell profile; add it.

**`ModuleNotFoundError: No module named 'compas'`** — you ran `python foo.py`
instead of `uv run foo.py`. That is the single most common error in this
course. Always `uv run`.

**A viewer window opens then immediately closes / crashes** — this is a
graphics-driver issue, not a Python one. Every viewer example in this repo has
a headless equivalent that writes a `.json` file instead; from Week 06 that is
the primary mode anyway.

**Something is broken in a way you cannot name** — nuke and rebuild. It is
fast and it is not a defeat:
```bash
rm -rf .venv && uv sync
```

**Git said something you don't understand** — the ten common cases and their
three-line recoveries are in
[rccn wiki ▸ Git for coursework ▸ What can go wrong](https://kb.rccn.dev/computation/development-environment/version-control/coursework-git#what-can-go-wrong).
Merge conflicts, rejected pushes, authentication failures, accidental secret
commits — all named, all recoverable.

**Still stuck** — open an issue on the course repo with the *exact* command you
ran and the *complete* error output. "It doesn't work" is unanswerable; a
traceback is usually self-answering, and pasting one is how you learn to read
them.
