# How the lectures are organised

`Lecture_N` is Week N. Each concept sits in the first week that has everything it
needs, so the weeks read in order.

| Part | Week | The concept | Builds on |
| ---- | ---- | ----------- | --------- |
| **I. Literacy** | [01](Lecture_01/README.md) | the toolchain: Python, git, `uv`, an assistant | |
| | [02](Lecture_02/README.md) | values, types, lists, functions | 01 |
| | [03](Lecture_03/README.md) | control flow, modules, debugging | 02 |
| | [04](Lecture_04/README.md) | dictionaries; points, frames, transformations in COMPAS | 03 |
| **II. Geometry as data** | [05](Lecture_05/README.md) | **mesh**: vertices joined into faces | 04 |
| | [06](Lecture_06/README.md) | **graph**: a mesh without faces, only connections | 05 |
| | [07](Lecture_07/README.md) | **class**: a data structure of your own | 04 |
| | [08](Lecture_08/README.md) | **recursion**: a function defined by itself | 03 |
| | [09](Lecture_09/README.md) | **timber model**: classes in a graph, in a real library; files and JSON; core → artifact → adapter; a project to hold it | 06, 07 |
| **III. Algorithms** | [10](Lecture_10/README.md) | **geometric algorithms**, and testing them | 05, 06 |
| | [11](Lecture_11/README.md) | **simulation**: arrays of cells, then agents as objects | 07, 10 |
| | [12](Lecture_12/README.md) | **optimization** and **learning** | 10 |
| **IV. Engineering** | [13](Lecture_13/README.md) | **review**: it is right, is it good? | 09, 10 |
| | [14](Lecture_14/README.md) | **shipping** a plugin with ghuser-builder | 09, 13 |
| | [15](Lecture_15/README.md) | **working with AI**: one stage of a pipeline that exists | 09, 10, 13, 14 |

The dates are in the [schedule](../README.md#schedule-2026-fall).

## Inside a week

Every week has the same shape. Not every week has every folder.

```
Lecture_06/
├── README.md       the lecture: start here
├── examples/       short scripts, one idea each, in the order of the lecture
├── applications/   a whole design problem, from data to answer
├── notebooks/      the ideas step by step; its README lists them, fundamentals first
├── figures/        make_figures.py, and the SVGs it draws from the real code
├── data/           input files
├── tests/          property tests of the examples (W10–12)
└── checkpoints/    your self-check: uv run check.py 06 (W01–09)
```

Run anything from the repo root: `uv run Lecture/Lecture_06/examples/01_graph_from_scratch.py`.

[`shared/`](shared/README.md) holds what the notebooks share. `obscure_examples/` is
older material, kept but not part of the course.

## Threads that cross the weeks

**The architecture**, from Week 09 on: pure core → JSON artifact → thin adapter. Most
strong final projects are one algorithm from Part III in that shape.

**Engineering.** Each step needs the one before it:

| Week | Step | The question |
| ---- | ---- | ------------ |
| [09](Lecture_09/README.md#part-d--a-project-that-can-hold-components) | scaffold, spec, dev, test | where does everything live? |
| [10](Lecture_10/README.md#part-b--testing) | testing | how do you know it is right? |
| [13](Lecture_13/README.md) | review | it is right. Is it *good*? |
| [14](Lecture_14/README.md) | shipping | how does it reach someone else's Grasshopper? |
| [15](Lecture_15/README.md) | AI | which of these steps can a machine take? |

AI comes last on purpose: an assistant can write the middle of this pipeline, and can
only be trusted to once the two ends exist, a test that says what correct means and a
reviewer who can tell good from passing.

**Three questions run through Part III:**

1. **How do you know it is right?** A theorem, a known case, an invariant, a comparison
   with brute force. Never "the picture looks right".
2. **What does it cost?** The convex hull and nearest neighbours are where *how* you
   compute something decides whether you can compute it at all.
3. **Is one run evidence?** Simulations and stochastic searches vary from run to run, so
   their tests average over seeds and compare under equal budgets.

## How to run a notebook

**Once per clone**, so notebook outputs never end up in your commits:

```bash
uv run nbstripout --install
```

**Each time:**

```bash
uv run Lecture/shared/copy_to_mywork.py 05      # copy Week 05's notebooks into MyWork/
uv run jupyter lab MyWork/notebooks                 # opens them in your browser
```

Open a notebook and run the cells from the top, one at a time, with
`Shift` + `Enter`. When you are done, stop the server with `Ctrl` + `C` in the
terminal.

Good to know:

- **Work on the copies in `MyWork/notebooks/`**, not the originals: those are
  updated by the instructor, and editing them causes merge conflicts on
  `git pull upstream main`. Copy one notebook with `05/02`, everything with
  `all`. A copy brings its pictures with it. It is never overwritten, unless
  you add `--force` (do that to pick up the instructor's updates; your edits
  in that copy are lost). The copies are not committed: `MyWork/notebooks/`
  is in `.gitignore`.
- **The compas_timber notebooks** (Week 09) need
  `uv run --extra timber jupyter lab MyWork/notebooks`.
- **VS Code** works too: open the `.ipynb` and choose this project's `.venv`
  as the kernel. If a 3D view stays blank there, use the browser. Zed does not
  open notebooks.
