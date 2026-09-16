# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Course materials for **ARCH3045 — Design Computation and Computational
Geometry** (COMPAS-based computational geometry, algorithms, and
digital-fabrication workflows). It is not a single application; it is a
tree of independent, mostly-standalone scripts organized by week:

- `Lecture/Lecture_NN/` — lecture code, each with its own `README.md`
- `Exercise/Lecture_NN/` — in-class exercises
- `Assignment/N_*/` — the final project (`5_Final_Project`, the whole grade,
  100%), the ungraded agentic-workflow lab (`6_agentic_workflow`),
  the `0_copilot` setup gate, and retired legacy assignments (superseded by the
  W01–09 checkpoints; kept as optional practice)
- `Practices/` — scratch/practice scripts, some with `*_test.py` companions
- `Reference/` — external reference material (e.g. a cloned repo)

There is no shared library code, build step, or app entry point tying these
together — `main.py` at the root is just the placeholder from `uv init` and
is not used by the course content. Treat each script as its own unit; do not
assume imports work across lecture/assignment folders (a few exceptions are
noted below).

## Environments

**`uv` is the primary toolchain** (Python ≥3.13, `pyproject.toml` + `uv.lock` at
repo root). As of Fall 2026 the course moved off conda/VS Code onto uv/Zed;
Weeks 01–14 are uv-only.

```bash
uv sync                  # build/repair the env from the lockfile
uv run <script>.py       # run a script inside it (never bare `python`)
uv run check.py          # the course self-check runner (see below)
uv add <package>         # add a dependency; commit pyproject.toml AND uv.lock
```

Run everything from the repo root — `check.py` and the checkpoint imports
assume that working directory.

**conda is legacy.** `environment.yml`, `environment_ml.yml` and
`environment_neural.yml` remain for the Week 15+ ML/neural material and for
older student projects. Do not use them for Weeks 01–14, and do not mix the two
in one project. Older lecture READMEs that said `conda install compas` have been
rewritten; if you find a surviving one, it is stale.

## The checkpoint system

Weeks 01–09 are checkpoint-driven and self-contained: each lecture folder has a
full tutorial in its `README.md` plus a `checkpoints/` directory:

```
Lecture/<folder>/checkpoints/
├── tasks.py           # student edits this; functions raise NotImplementedError
├── conftest.py        # one-line sys.path bridge so spec/ can import tasks
└── spec/
    └── test_tasks.py  # the spec, written as pytest; students are told to read it
```

The spec was moved into `spec/` on 2026-09-10 so students see one clearly-
editable file at the checkpoints/ root and cannot accidentally edit the
read-only test by clicking a visual sibling. `conftest.py` is what keeps
`from tasks import …` working across the split — do not delete it. Every
`spec/test_tasks.py` also carries a READ ONLY banner at line 1.

Week 06 is the exception — it ships `core.py` + `runner.py` instead of
`tasks.py`, because the whole lesson is that those are separate layers.
Same `spec/` split applies.

`check.py` at the repo root runs a week's checkpoints via an in-process pytest
plugin and prints PASS / FAIL / TODO (TODO = still raising `NotImplementedError`).

**Week → folder mapping is NOT the folder number.** The `COURSE` list at the top
of `check.py` is the authority, and `README.md`'s schedule is the student-facing
one:

| Week | Folder | Week | Folder |
| ---- | ------ | ---- | ------ |
| 01 | `Lecture_00` | 06 | `Lecture_06` |
| 02 | `Lecture_01` | 07 | `Lecture_08` |
| 03 | `Lecture_02` | 08 | `Lecture_07` |
| 04 | `Lecture_04` | 09 | `Lecture_05` |
| 05 | `Lecture_03` | | |

`Lecture_06` was repurposed from `compas_vol` (now parked in
`Lecture_06/optional_compas_vol/`, excluded from the 2026 syllabus) to hold the
new software-engineering lecture.

### If you add or edit a checkpoint

Two things must both hold, and it is worth actually running them:

1. The shipped stub produces `TODO`/`FAIL` (never accidental `PASS`).
2. A correct implementation produces all `PASS` — i.e. the spec is satisfiable.

When swapping a reference solution in to check (2), make sure the restore of the
stub runs even when the check fails; a `set -e` script will otherwise abort
mid-way and leave the solution committed in place of the stub.

Several specs deliberately encode a decision the task docstring leaves open
(what `list_stats([])` does, which key wins in `invert`, how a flat mesh is
coloured). That is intentional teaching: the prose is vague, the spec decides.
Do not "fix" the vagueness by making both agree.

## Tests

Tests are colocated with the code they check and run per-file with pytest —
there is no single repo-wide suite. For Weeks 01–09 prefer `uv run check.py
<week>`, which wraps pytest with per-checkpoint output.

```bash
pytest path/to/test_foo.py -v          # run one test file
pytest path/to/test_foo.py::test_name  # run one test
uv run pytest Lecture/Lecture_12/test_wall.py -v   # if using the uv env
```

Examples: `Practices/is_palindrome_test.py`, `Lecture/Lecture_12/test_staircase.py`,
`Lecture/Lecture_12/test_wall.py`, `Lecture/Lecture_12/test_staircase.py`.

Geometry tests in this repo follow a deliberate style (see
`Lecture/Lecture_12/test_staircase.py`, which is itself a teaching example):
test **properties**, not exact shapes (counts, monotonicity, no gaps/overlaps,
bounding-box facts) — never assert pixel-perfect geometry. Never compare
floats with `==`; use `pytest.approx`. Also test the failure path (invalid
input should raise, not silently return junk).

In `Lecture_12`, a test file can itself *be* the assignment spec written
before any implementation exists (see `test_wall.py`) — don't assume a
missing implementation module is a bug; it may be intentional, to be filled
in by `tdd_agent.py` or by the student.

## Architecture notes specific to this repo

### COMPAS is the geometry kernel throughout
Nearly every script imports `compas.geometry` (Box, Frame, Point, Vector,
Transformation, etc.) and, for visualization, `compas_viewer`. Scripts
commonly branch on `compas.is_grasshopper()` to support both a
`compas_viewer` desktop preview and Grasshopper/Rhino execution from the same
file — see `Exercise/2_re-write_to_oop/example_random_walker.py` for the
pattern.

### The "pure core / artifact / adapter" layering (Lecture 12)
Later material formalizes a 3-layer pattern that recurs across
assignments — worth knowing before touching anything under `Lecture_12/` or
`Assignment/6_agentic_workflow/`:
1. **Core** — a pure Python+COMPAS function/module (numbers in, geometry
   out; no file IO, no viewer, no Rhino). Testable and reusable anywhere.
2. **Artifact** — the verified result serialized to COMPAS JSON
   (`output/*.json`), produced headlessly and viewable via `compas_viewer`
   before Rhino is ever involved.
3. **Adapter** — a thin script (`rhino_load.py`) run inside Rhino 8's
   ScriptEditor that only loads and converts the artifact; it contains no
   design logic.
Keep intelligence out of the host application (Rhino/Grasshopper); develop
and verify headlessly, and let Rhino only receive finished results.

### Lecture 12 `plugin_set/` — the worked Grasshopper deploy example
`Lecture/Lecture_12/plugin_set/` (`compas_studio`) is a complete, runnable
example of the Week 14 deploy story: a Grasshopper plugin set developed and
tested entirely outside Rhino.
- `src/compas_studio/` — pure COMPAS cores (wall, staircase, grid); **no**
  `rhinoscriptsyntax`/`import Rhino`, so they run and are tested headlessly.
- `tests/` — pytest specs; run with `uv run pytest Lecture/Lecture_12/plugin_set/tests`
  (a local `conftest.py` puts `src/` on the path; CI uses `pip install -e .`).
- `components/Cs_*/` — GH component sources (`code.py` + `metadata.json` +
  24×24 `icon.png`) in the exact layout the
  [COMPAS componentizer](https://github.com/compas-dev/compas-actions.ghpython_components)
  expects. Each `code.py` is a thin adapter importing one core function.
- `.github/workflows/` — `test.yml` (CI, Linux, pytest) and `build.yml` (CD,
  `windows-latest`, `compas-dev/compas-actions.ghpython_components@v5`,
  `interpreter: cpython` for Rhino 8) building `.ghuser` files with no Rhino
  installed. These are a template — in a standalone repo they live at the repo
  root `.github/workflows/`, not in a subfolder.
- The icons are real PNGs generated programmatically; if regenerating, keep
  them exactly 24×24 or the componentizer rejects them.

Note the deliberate teaching contrast: `Lecture_12/wall.py` is raw model output
(~150 lines, passes the tests, unreadable) while
`plugin_set/src/compas_studio/wall.py` is the reviewed 20-line version. Same
passing tests — the difference is what code review catches and tests cannot.
Don't "tidy" the messy one; it is the specimen.

### Lecture 11 / 12: hand-rolled agent harnesses (LLM-in-the-loop)
`Lecture/Lecture_11/` and `Lecture/Lecture_12/` build, from scratch, the kind
of coder/reviewer/tool-loop harness that tools like Claude Code implement —
this is explicitly the pedagogical point of those lectures, so if asked to
extend or debug them, preserve the pattern rather than "simplifying" it away:
- `Lecture_11/llm.py` centralizes the connection to the course's
  self-hosted, OpenAI-protocol-compatible LLM node (`llm-api.rccn.dev`,
  model `gemma-4-26B-A4B-it-AWQ-4bit`); every other script in that folder
  imports `get_client()`/`chat()` from it rather than talking to the API
  directly. It reads `DCCG_LLM_KEY` from a local `.env` (copy
  `.env.example` → `.env`; never commit a real `.env`).
- The core loop (`03_agent_loop.py`) is: harness sends messages+tools to the
  model → model may request a tool call → **harness** (never the model)
  executes it → result is appended to the message history → repeat until
  done, bounded by a `MAX_STEPS` budget. `temperature=0` is deliberate
  (reproducibility / to curb small-model hallucination), not an oversight.
- `04_coder_reviewer.py` and `05_mini_harness.py` execute LLM-generated code
  and shell commands on the real filesystem, gated by a **human approval
  step** before anything runs. The `--auto` flag skips that gate and exists
  only for classroom demos — treat any request to use `--auto` outside that
  context as something to flag, not do by default. `05_mini_harness.py`
  additionally confines file/shell access to its own `./workspace`.
- `Lecture_12/tdd_agent.py` replaces the LLM reviewer with pytest: it writes
  an implementation, runs the test file against it, and feeds failures back
  verbatim until green — a stricter, non-arguable version of the same loop.

`Assignment/6_agentic_workflow/` is an ungraded required lab that *drives* these
scripts (`04_coder_reviewer.py`, and optionally `tdd_agent.py`) rather than
containing its own implementation — its outputs are a brief, an iteration log,
`# REVIEW:` comments on generated code, and a reflection, not new source code.
The course grade is the final project (100%); completing the W01–09 checkpoints
is a required gate but is not scored. Exercises and milestone labs are ungraded
preparation.
