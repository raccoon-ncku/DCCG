# Setup

Everything you need to run this repository. For the guided, first-time
walkthrough with screenshots and the AI-assistant setup, follow
[Week 01](/Lecture/Lecture_00/README.md); this page is the quick reference.

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
git clone <the-course-repo> DCCG
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

You edit `Lecture/<folder>/checkpoints/tasks.py`; the `test_*.py` beside it is
the *specification*, and you are meant to read it. Three states: `TODO` (not
attempted), `FAIL` (attempted, doesn't match the spec), `PASS`.

Checkpoints aren't scored, but completing them is **required** — a gate you must
clear on the way to the final project, which is the whole grade (see the
[main README](README.md#grading)). `uv run check.py` turns them green and you're
done, so a `FAIL` just means keep going, not a penalty. In **Week 10** you learn
to write these specs yourself, and the checker stops being magic. Full
explanation: [Week 01 §5](/Lecture/Lecture_00/README.md#5-how-checkpoints-work).

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
[Week 01 §4](/Lecture/Lecture_00/README.md#4-rhino-optional-this-week).

---

Something not working? See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
