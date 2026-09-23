# Final Project — Fall 2026

## The brief

**Write a Python-based Grasshopper plugin, with the help of AI — and make it
professional, reproducible, and maintainable.**

That is the whole assignment. Pick a piece of parametric geometry worth turning
into a reusable component (a wall bond, a stair, a packing tool, a facade
pattern — anything with real logic), and build it the way this course has taught:

- **Professional** — a pure COMPAS core with no Rhino imports, plus a thin
  Grasshopper adapter. Not a script that draws one nice picture; a *tool*
  someone else could install and use.
- **Reproducible** — it runs headlessly (no Rhino needed) and produces the same
  verified result every time, with tests that prove it and CI that runs them.
- **Maintainable** — clear structure, readable code you can explain, and a build
  pipeline so a new version is one command, not a manual export.

Use AI freely to write it — that is the point of the course — but you own every
line, and "professional / reproducible / maintainable" is exactly the standard
that separates directing an agent from blindly following one.

The recommended route is the **Grasshopper plugin set** built with the COMPAS
componentizer pipeline from Week 14 (worked example:
[`Lecture/Lecture_12/plugin_set/`](/Lecture/Lecture_12/plugin_set/README.md)). A
Rhino `.rhp` plugin or a standalone CLI/library with a loader script are also
fine — the `.ghuser` set is just the most reusable and the one the lectures
build toward.

## Required architecture

This is the non-negotiable part, and it is what the whole semester built toward:

```
your-project/
├── core/                  # 1. CORE — pure Python + COMPAS
│   └── <your_module>.py   #    numbers in, geometry out
│                          #    NO viewer, NO file IO, NO `import rhino*`
├── tests/                 # pytest — the executable spec for your core
│   └── test_<module>.py
├── run.py                 # headless runner: core → output/*.json
├── output/
│   └── <artifact>.json    # 2. ARTIFACT — committed, reviewable
├── adapters/
│   ├── rhino_load.py      # 3. ADAPTER — runs in Rhino 8 ScriptEditor
│   └── gh_component.py    #    and/or a Grasshopper Python component
├── README.md              # what it does, how to install, how to run both ways
└── requirements / pyproject
```

The test for whether you got this right: **delete `adapters/` and your project
must still work.** Uninstall Rhino and your tests must still pass. If importing
your core requires Rhino, the architecture is wrong.

## Requirements

- Primary language is Python; geometry via COMPAS (other libraries welcome
  alongside it — `trimesh`, `numpy`, `shapely`, `networkx`, `pymoo`, …).
- The core is **parametric**: it takes arguments and behaves sensibly across a
  range of them, not just the one value in your screenshot.
- At least **6 meaningful tests** covering properties (counts, dimensions,
  monotonicity, no gaps/overlaps) and at least one failure path (invalid input
  raises rather than returning junk).
- A working adapter, demonstrated live in Rhino 8 or Grasshopper.
- A GitHub repository. Every member must have at least one commit.
- You may **not** copy an existing project wholesale. Referencing and rewriting
  is fine; cite what you referenced.

## Groups

Individually or in groups of up to 4. Group size does not change the bar, but
larger groups are expected to produce proportionally more.

## AI usage

Use AI assistants freely — that is the point of this course. The three course
rules apply, and they are enforced at the presentation:

1. **You must be able to explain every line.** You will be asked to, live.
2. **Disclose** — keep meaningful prompts in comments or a `log.md`.
3. **Verify, don't trust** — "it looked right in the viewer" is not evidence.
   Your tests are.

"The AI wrote it" is not a defence for code you cannot explain. If you
submitted it, you own it.

## Milestones

| When | Milestone |
| ---- | --------- |
| W10 · 2026.11.11 | Brief released — start thinking |
| W12 · 2026.11.25 | **Proposal + in-class pitch** (2 min): what it does, who'd use it, what the core function signature looks like |
| W14 · 2026.12.09 | **Iteration 1 review** — core + tests running headless |
| W16 · 2026.12.23 | **Iteration 2 review** — adapter working in Rhino/GH |
| W17 · 2026.12.30 | **Feature freeze** — no new features; docs, tests, packaging only |
| W18 · 2027.01.06 | **Final presentation + live demo** |

## Deliverables

- The GitHub repository, matching the structure above
- `README.md` with install + run instructions for **both** modes
- The committed artifact (`output/*.json`)
- Images or video of the result, in both headless and Rhino/GH contexts
- A short reflection (~300 words): where the AI helped, where it misled you,
  and what your tests caught that your eyes did not

## Assessment

**This project is your entire grade (100%).** The only other requirement is
completing the Weeks 01–09 checkpoints — a gate, not a scored component
([grading](/README.md#grading)). There is no point breakdown within the project;
it is judged as a whole against these criteria:

- **Runs headless** — a pure core plus a committed artifact, no Rhino required.
- **Runs inside Rhino 8 / Grasshopper** — through a thin adapter that adds no
  design logic.
- **Verifiably correct** — meaningful tests, ideally running in CI.
- **Well-built** — clear structure, sane names, honest documentation.
- **Presented well** — a live demo that shows both modes working.

These are not a checklist to tick — they describe what a good project shows. A
modest tool that is genuinely well-built, tested, and runs in both modes beats
an ambitious one that only works on the author's laptop with Rhino open. And
**process is worth more than the artifact** — the same rule as the agentic lab,
applied to the whole project.

## Deadline and submission

- **Presentation**: 2027.01.06, in class
- **Repository frozen**: 2027.01.10 23:59
- Submit the repository URL via Moodle

## Ideas and inspiration

- A wall / facade / bond generator with real fabrication constraints
- A stair or ramp generator that validates against building-code rules
- A packing or nesting tool for sheet-material fabrication
- A structural sizing tool driven by an optimizer (see [Lecture 09](/Lecture/Lecture_15_optimization/README.md))
- A mesh-relaxation or form-finding component
- A pathfinding / circulation analysis tool on a Graph
- A semantic image search over a reference library (see [Lecture 10](/Lecture/Lecture_10/README.md))
- An L-system / recursive growth system with fabrication-aware output

Good projects usually come from a real annoyance you have had in Rhino — a
thing you did by hand fifty times and wished were a button.
