# Setup

The quick reference. The first-time walkthrough is [Week 01](/Lecture/Lecture_01/README.md).

## Toolchain

| Job | Tool |
| --- | ---- |
| Python + packages | [`uv`](https://astral.sh/uv) (Python 3.13) |
| Editor | [Zed](https://zed.dev) (VS Code works too) |
| Version control | git + GitHub |
| Geometry | COMPAS 2.x |
| Grasshopper components | Rhino 8, and Docker to build them |

If an older tutorial says `conda install compas`, ignore it.

## First run

```bash
git clone https://github.com/raccoon-ncku/DCCG.git DCCG
cd DCCG
uv sync            # build the environment from uv.lock — do this once, first
uv run check.py    # confirm it works: your progress across every week
```

You never activate the environment. Prefix commands with `uv run`.

| Command | Does |
| ------- | ---- |
| `uv sync` | build/repair the environment to match the lockfile |
| `uv run <script>.py` | run a script inside the environment |
| `uv run check.py` | your checkpoint progress (see below) |
| `uv add <package>` | add a dependency (commit `pyproject.toml` **and** `uv.lock`) |

## Checkpoints

```bash
uv run check.py        # overview across every week
uv run check.py 05     # work on Week 05, with hints
uv run check.py 05 -v  # ... and full failure output
```

You edit the gitignored `answers.py`, which is copied from the `tasks.py` starter on
first run. The spec is `checkpoints/spec/test_tasks.py`: read it. Delete `answers.py`
to reset. Not scored, but required: [Week 01 §5](/Lecture/Lecture_01/README.md#5-how-checkpoints-work).

## Notebooks (Week 04 onward)

Notebooks live with their week, in a `notebooks/` folder beside that week's
README. Once per clone:

```bash
uv run nbstripout --install                         # keeps notebook outputs out of your commits
```

Then, for a week's notebooks:

```bash
uv run Lecture/shared/copy_to_mywork.py 05      # copy them into MyWork/
uv run jupyter lab MyWork/notebooks                 # open them in your browser
```

Details: [how to run a notebook](Lecture/README.md#how-to-run-a-notebook). Each `notebooks/` folder has a README listing what is in it.

## The one conda environment left

`environment_neural.yml` is only for the optional Week 15 diffusion / CLIP examples
(`Lecture_15/neural`). Never mix it with `uv` in the same project.

## Rhino and Docker

Install Rhino 8 and authenticate against the class licence server:
[Week 01 §4](/Lecture/Lecture_01/README.md#4-rhino-optional-this-week). Building
components needs Docker: [Week 09 D5](/Lecture/Lecture_09/README.md#d5-next-the-adapter-and-the-build).

## Git for this course

You **read from** the instructor's repo and **write to** a fork of your own.

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

**Your work goes in [`MyWork/`](MyWork/README.md).** The instructor never touches it, so
`git pull` never conflicts with it. Anything that must stay on your laptop goes in
`Notes/`, which is gitignored.

When a pull brings a new checkpoint stub, delete your `answers.py` and re-run, or copy
the new function in by hand.

**When something goes wrong:** the failure catalogue is on the
[wiki](https://kb.rccn.dev/computation/development-environment/version-control/coursework-git#what-can-go-wrong).

---

Something not working? See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
