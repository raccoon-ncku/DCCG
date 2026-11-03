# Week 01 — Toolchain: uv, Zed, git, and an AI assistant

By the end of today you have a working Python environment, an editor, a git
identity and an AI assistant, and one command proves it:

```bash
uv run check.py 01
```

## 1. The tools

| Job | Tool | Why |
| --- | ---- | --- |
| Python + packages | **uv** | one tool, fast, and it *locks* exact versions so your machine and mine agree |
| Editor | **Zed** | fast, and its AI shows you diffs to accept or reject |
| Version control | **git** | the record of what you did |

**`uv`** installs Python itself, creates a `.venv/` next to your code, installs the
packages in `pyproject.toml`, pins them in `uv.lock`, and runs your code inside that
environment with `uv run`. You never activate anything.

> Older tutorials say `conda`. If you have it installed, leave it alone, but do not
> use it here: mixing the two is the most common cause of "it works for you but not
> for me". `environment_neural.yml` is only for the optional Week 15 models.

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
  Week 15; you do not need one yet.

You get a key for the **course LLM node** (`llm-api.rccn.dev`) in Week 15.

## 3. Get the repository

```bash
git clone https://github.com/raccoon-ncku/DCCG.git DCCG
cd DCCG
uv sync
```

**Week 01 is local-only:** commit A0 locally, no push. Next week we set up a fork:
[SETUP ▸ Git for this course](/SETUP.md#git-for-this-course).

### Your work vs. the instructor's

| | Path | Whose | Rule |
| --- | --- | --- | --- |
| Instructor's | `Lecture/…/README.md`, `Reference/…` | theirs | you read, sometimes edit (checkpoint stubs) |
| Yours | [`MyWork/`](/MyWork/README.md) | yours | put notes, sketches, practice here |
| Private | `Notes/` | yours, laptop-only | gitignored — never pushed |

The instructor never writes into `MyWork/`, so `git pull` never conflicts with it.

### Useful uv commands

| Command | What it does |
| ------- | ------------ |
| `uv sync` | Build/repair the environment to match the lockfile |
| `uv run <script.py>` | Run a script inside the environment |
| `uv add <package>` | Add a dependency (updates `pyproject.toml` + `uv.lock`) |
| `uv remove <package>` | Remove one |
| `uv tree` | Show what is installed and why |

### Check your laptop can do the work

In [`MyWork/`](/MyWork/README.md), create `hello.py`:

```python
from compas.geometry import Point, Vector

print(Point(1.0, 2.0, 3.0) + Vector(0.0, 0.0, 1.0))
```

```bash
uv run MyWork/hello.py          # Point(x=1.000, y=2.000, z=4.000)
```

`ModuleNotFoundError: No module named 'compas'` means you ran `python` instead of
`uv run`.

## 4. Rhino (optional this week)

Download Rhino 8 from <https://www.rhino3d.com/download>. When prompted for a
licence, choose **`zoo`** as the authentication method and **`zoo.rccn.dev`**
as the server. It covers Rhino 6 and 8, Windows and Mac.

> The licence server is reachable only from the computer lab's wifi and from
> Workspace Raccoon.

The Python weeks run without Rhino. You need it from the first component on.

## 5. How checkpoints work

Each week ships with **checkpoints**, small and precisely specified tasks, and a
runner that tells you whether you have them right:

```bash
uv run check.py        # overview of every week
uv run check.py 01     # this week, with hints
uv run check.py 01 -v  # ... and the full failure output
```

```
Lecture/<folder>/checkpoints/
├── tasks.py         ← STARTER  ─┐  (or core.py + runner.py in Week 09)
│                                │  read-only; git-tracked
│                    auto-copied ├─ every `git pull` refreshes it
│                                │
├── answers.py       ← YOU EDIT ─┘  (or answers_core.py + answers_runner.py)
│                                   gitignored; never conflicts on pull
├── conftest.py                     ← plumbing, ignore
└── spec/
    └── test_tasks.py               ← READ ONLY — the specification
```

The first `uv run check.py NN` copies `tasks.py` to `answers.py`. Edit `answers.py`;
`tasks.py` stays clean, so `git pull upstream main` never conflicts with your work.
Delete `answers.py` to start again.

**Read the spec.** `spec/test_tasks.py` is the precise statement of what your code
must do.

Three states:

| | meaning |
| - | ------- |
| `TODO` | not attempted yet — the stub still raises `NotImplementedError` |
| `FAIL` | attempted, but does not match the spec |
| `PASS` | correct |

A `FAIL` is not a penalty. Checkpoints are not scored, but completing them is
required: they are your gate to the final project, which is the whole grade.

### Using AI on checkpoints

Allowed, and encouraged, but **you must be able to explain every line you submit.**
Try it yourself first, then ask the AI, then diff the two and work out who was right.

## 6. This week's checkpoints

Four of the five checks verify your install. The fifth asks you to edit one line in
`Lecture/Lecture_01/checkpoints/answers.py`: `student_name()` returns your name.

```bash
uv run check.py 01
```

When all five pass, commit locally:

```bash
git add -A
git commit -m "Week 01: environment set up"
```

That commit is assignment [A0](/Assignment/0_copilot/README.md).

## 7. Troubleshooting

See [TROUBLESHOOTING.md](/TROUBLESHOOTING.md).
