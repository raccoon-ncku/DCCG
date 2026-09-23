# Setup

Everything you need to run this repository. For the guided, first-time
walkthrough with screenshots and the AI-assistant setup, follow
[Week 01](/Lecture/Lecture_01/README.md); this page is the quick reference.

## Toolchain

| Job | Tool |
| --- | ---- |
| Python + packages | [`uv`](https://astral.sh/uv) (Python 3.13) |
| Editor | [Zed](https://zed.dev) (VS Code works too) |
| Version control | git + GitHub |
| Geometry | COMPAS 2.x |
| 3D (from Week 14, optional) | Rhino 8 / Grasshopper |

We use `uv` and Zed this year. If you find an older tutorial that says
`conda install compas`, ignore it.

## First run

```bash
git clone https://github.com/raccoon-ncku/DCCG.git DCCG
cd DCCG
uv sync            # build the environment from uv.lock — do this once, first
uv run check.py    # confirm it works: your progress across every week
```

You never activate the environment. Prefix commands with `uv run` instead — it
can never pick the wrong Python by accident.

| Command | Does |
| ------- | ---- |
| `uv sync` | build/repair the environment to match the lockfile |
| `uv run <script>.py` | run a script inside the environment |
| `uv run check.py` | your checkpoint progress (see below) |
| `uv add <package>` | add a dependency (commit `pyproject.toml` **and** `uv.lock`) |

## How the course works: checkpoints

Weeks 01–09 are checkpoint-driven. Each week's folder holds a self-contained
tutorial, commented examples, and **checkpoints** — small, precisely specified
tasks with an automatic checker.

```bash
uv run check.py        # overview across every week
uv run check.py 05     # work on Week 05, with hints
uv run check.py 05 -v  # ... and full failure output
```

On first `check.py NN` for a week, the runner copies the shipped starter
`tasks.py` to a gitignored `answers.py`. **You edit `answers.py`**; the
starter stays clean so `git pull upstream main` never conflicts with your
work. The spec at `checkpoints/spec/test_tasks.py` (one folder down, marked
READ ONLY) is the *specification*, and you are meant to read it. Three
states: `TODO` (not attempted), `FAIL` (attempted, doesn't match the spec),
`PASS`. Delete `answers.py` at any time to reset from the current starter.

Checkpoints aren't scored, but completing them is **required** — a gate you must
clear on the way to the final project, which is the whole grade (see the
[main README](README.md#grading)). `uv run check.py` turns them green and you're
done, so a `FAIL` just means keep going, not a penalty. In **Week 10** you learn
to write these specs yourself, and the checker stops being magic. Full
explanation: [Week 01 §5](/Lecture/Lecture_01/README.md#5-how-checkpoints-work).

## Legacy conda environments

`environment.yml`, `environment_ml.yml` and `environment_neural.yml` remain only
for the Week 15+ ML/neural material and for anyone continuing a previous year's
project. They are **not needed for Weeks 01–14**. Do not mix them with `uv` in
the same project — that is the most common cause of "it works for you but not
for me".

## Rhino (optional until Week 14)

The course runs entirely without Rhino; the JSON artifact is the primary output
from Week 06 on. When you do want it, install Rhino 8 and authenticate against
the class licence server — details in
[Week 01 §4](/Lecture/Lecture_01/README.md#4-rhino-optional-this-week).

## Git for this course

You **read from** the instructor's repo (updates every week) and **write to** a
fork of your own. Two remotes, one clone. This becomes the backbone of the
course: your commits *are* the record of what you did, your fork *is* your
final-project submission at the end.

**Week 01** is local-only: clone from the instructor's URL, commit A0 locally.
Nothing to push yet.

**From Week 02** the setup is fork-based:

```bash
# 1. Fork raccoon-ncku/DCCG on GitHub (browser, one click)
# 2. In your terminal, from a fresh clone of YOUR fork:
git remote add upstream https://github.com/raccoon-ncku/DCCG.git
git remote -v                             # confirm origin AND upstream are listed
```

Then the weekly loop is four commands:

```bash
git pull upstream main                    # get the instructor's new material
git add MyWork/week03-notes.md            # stage your work
git commit -m "Week 03: notes + checkpoint 4 attempt"
git push                                  # publish to your fork
```

**Your own work goes in [`MyWork/`](MyWork/README.md)** — a top-level folder
reserved for you. The instructor never adds, edits, or deletes files there, so
`git pull` never conflicts with it. Put practice, notes, sketches, and scratch
here. For files you want kept strictly on your laptop and *not* committed, use
`Notes/` instead — it's gitignored.

**`git pull` never conflicts with your checkpoint work.** You edit
`checkpoints/answers.py`, which is gitignored; the instructor only ever
touches `checkpoints/tasks.py` (the read-only starter). When a pull brings
in a new checkpoint stub, delete your `answers.py` and re-run to pick it up
(or copy the new function's `raise NotImplementedError` line in by hand).

**When something goes wrong** — merge conflict, rejected push, "I committed to
the wrong branch", accidental `.env` push — see the failure catalogue in
[rccn wiki ▸ Git for coursework](https://kb.rccn.dev/computation/development-environment/version-control/coursework-git#what-can-go-wrong).
It is ten failure modes with the three-line recovery for each. Read once now,
come back to it in Week 04.

---

Something not working? See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
