# compas_studio — a worked Grasshopper plugin set

This is the reference example for the Software Engineering weeks (10, 13, 14):
a small but **complete** Grasshopper plugin set that is developed, tested, and
deployed *entirely outside Rhino*. Three components — a running-bond wall, a
staircase, a grid mesh — the same cores you built earlier in the course, now
packaged the way a studio would actually ship them.

Read it as the answer to a question the whole semester has been building toward:
**how does pure Python geometry become a plugin someone else can install — and
how do you keep it correct while an AI writes half of it?**

## The shape of it

```
plugin_set/
├── src/compas_studio/        1. CORE — pure Python + COMPAS, no Rhino
│   ├── wall.py               │   running_bond_wall()
│   ├── staircase.py          │   straight_staircase()
│   └── grid.py               │   grid_mesh()
├── tests/                    2. SPEC — pytest, runs headless in CI
│   ├── test_wall.py
│   ├── test_staircase.py
│   └── test_grid.py
├── components/               3. ADAPTERS — one folder per GH component
│   ├── Cs_RunningBondWall/   │   code.py + metadata.json + icon.png
│   ├── Cs_Staircase/         │   each code.py just calls the core
│   └── Cs_GridMesh/
└── .github/workflows/        4. PIPELINE
    ├── test.yml              │   every push: run the tests (Linux, no Rhino)
    └── build.yml             │   every tag:  build .ghuser files (Windows, no Rhino)
```

Four layers, one rule holding them apart: **the core knows nothing about
Rhino, and Rhino only ever receives results.** Grep the whole `src/` tree for
`rhinoscriptsyntax` or `import Rhino` — you will find nothing. That absence is
what makes every good thing below possible.

## Why "outside Rhino" is the entire trick

The usual way to write a Grasshopper component is to open Grasshopper and type
Python into a GHPython node. That code:

- cannot be tested (it only runs inside a running Rhino document),
- cannot be version-controlled sensibly (it lives inside a binary `.gh` file),
- cannot be built by CI, and an agent cannot see whether it worked,
- and reaches for `rhinoscriptsyntax`, welding it to Rhino forever.

We invert it. The geometry lives in `src/compas_studio/` as ordinary COMPAS
functions. COMPAS geometry is plain Python objects — a `Box` is a `Box` whether
or not Rhino exists — so the core runs, and is **tested**, on any machine. The
Grasshopper component becomes a four-line adapter that imports one function and
converts its output. Look at `components/Cs_RunningBondWall/code.py`: there is
no geometry logic in it to be wrong.

## Run the tests (the verify stage)

From the repo root:

```bash
uv run pytest Lecture/Lecture_12/plugin_set/tests -q
```

15 property tests — counts, monotonic ascent, nothing floating, no brick past
the wall's end, correct Euler characteristic, and every function rejecting
nonsense input. No pictures asserted; if the invariants hold, the geometry is
right. This is exactly the `test.yml` job, which a Linux CI runner executes on
every push.

## Build the components (the deploy stage)

You do **not** build these on your laptop, and you do not need Rhino to build
them. `build.yml` runs the [COMPAS GHPython
componentizer](https://github.com/compas-dev/compas-actions.ghpython_components)
on a Windows CI runner. It reads each folder in `components/`, and writes a
matching `Cs_*.ghuser` file — the installable Grasshopper user object — fetching
the Grasshopper IO assembly through NuGet. No Rhino, no display, no manual step.

Trigger it by tagging a release:

```bash
git tag v0.1.0
git push --tags
```

The built `.ghuser` files appear as a downloadable artifact on the Actions run,
and are attached to the GitHub Release. A studio-mate installs them by dropping
them into their Grasshopper `UserObjects` folder — no repo, no Python, no setup.

> ⚠️ **A `.ghuser` forgets where it came from.** Once you drop a component into a
> Grasshopper document it becomes a plain GHPython node; a later release will
> **not** auto-update instances already placed in old files. Version
> deliberately, and tell your users what changed. (This is a real limitation of
> the format, worth knowing before you rely on it.)

## Each component's three files

| File | What it is | Who writes it |
| ---- | ---------- | ------------- |
| `code.py` | the adapter: import core → call → convert to Rhino | you / an agent |
| `metadata.json` | name, category, inputs, outputs, types | you |
| `icon.png` | a 24×24 icon for the GH ribbon | you (any image) |

The input and output names in `code.py`'s `RunScript(self, ...)` must match the
parameters declared in `metadata.json`, by name and count. That is the one
place the two files have to agree.

## How you extend it — and where the agent comes in

Adding a fourth component is the same loop every time, and it is the loop the
whole course has been teaching you to *run yourself* rather than hand to a
chatbot:

1. **Spec.** Write `tests/test_newthing.py` first — the executable brief.
2. **Core.** Implement `src/compas_studio/newthing.py` until the tests pass.
   This is the step you can safely delegate to an agent (Weeks 11–13): it is
   pure, and the tests are the reviewer that cannot be talked into approving.
3. **Review.** Read the code the agent wrote. Green tests prove it is
   *correct*; only you decide it is *good* — clear, no waste, sane names.
   Compare `src/compas_studio/wall.py` (reviewed) with `../wall.py` (raw model
   output) to see the gap tests do not catch.
4. **Adapter.** Add `components/Cs_NewThing/` — a thin `code.py`, a
   `metadata.json`, an icon.
5. **Ship.** Push (CI runs the tests), then tag (CI builds the `.ghuser`).

The point of doing it this way is not that it is fast. It is that **you
understand and can vouch for every stage** — which is the only thing that lets
you use an AI to go faster without shipping something you cannot stand behind.
The lecture in `../README.md` walks through this loop in full.
