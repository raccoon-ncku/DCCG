# compas_studio — a worked Grasshopper plugin set

This is the reference example for the Software Engineering weeks (10, 13, 14, 15):
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
├── pyproject.toml            what this is, which Python, which libraries
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
│   ├── Cs_Staircase/         │   each code.py finds the core, then calls it
│   └── Cs_GridMesh/
├── yak.json + icon.png       the package's description in Rhino's Package Manager
├── scripts/ghuser            4. BUILD — components/ -> dist/, with ghuser-builder
└── .github/workflows/        5. PIPELINE
    ├── test.yml              │   every push: run the tests (Linux, Python 3.9, no Rhino)
    └── build-ghuser.yml      │   every push: build + verify; every tag: release a .yak
```

It is the same shape as the [project template](../project_template/README.md)
you scaffold your own project from (Lecture 12, Part C), with three
components instead of one.

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
Grasshopper component becomes a short adapter that imports one function and
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
every push (on Python 3.9, the Python inside Rhino 8).

## Build the components (the deploy stage)

You do not need Rhino, Windows, or Grasshopper to build these. The build is
[**ghuser-builder**](https://git.rccn.dev/libs/ghuser-builder), the lab's
Docker image for it. Its one command, `ghuser-build`, does three things:

1. **componentize**: each folder in `components/` becomes a `Cs_*.ghuser`
   file, written by the [COMPAS componentizer](https://github.com/compas-dev/compas-actions.ghpython_components)
   with `GH_IO.dll`, the library Grasshopper itself uses;
2. **verify**: every `.ghuser` is opened again and checked against the
   source: name, parameters, embedded code. A mismatch fails the build;
3. **package**: the components and the core library go into one `.yak`,
   the file Rhino's Package Manager installs.

The same command runs in two places, and that is the point:

```bash
# 1. on your laptop (needs Docker), from plugin_set/
scripts/ghuser
ls dist dist/ghuser

# 2. on GitHub: every push builds and verifies; a tag also releases
git tag v0.1.0 && git push --tags
```

`dist/ghuser/Cs_*.ghuser` and `dist/compas-studio-<version>-rh8_0-any.yak`
appear locally (1), or attached to the GitHub Release (2). A studio-mate
installs the set by dragging the `.yak` onto Rhino 8: no repo, no Python, no
setup.

**How the core gets into Rhino.** A `.ghuser` holds only the adapter. The
core, `compas_studio`, is not on PyPI, so it travels **inside the `.yak`**
(`GHUSER_YAK_INCLUDE="src/compas_studio:lib/compas_studio"`, set in
`scripts/ghuser` and in the workflow). The lines at the top of every
`code.py`, down to the dashed line, find that `lib/` folder for the
component's own version and put it on Python's path. COMPAS itself comes from
the `# r: compas` line, which Rhino resolves.

**What is pinned, and why.** The image tag (in `scripts/ghuser` and
`build-ghuser.yml`) fixes the Grasshopper file library and the componentizer
version. A `.ghuser` written with a newer `GH_IO` than your users' Rhino is
the classic *component will not load* bug, so upgrading is a decision you
make on purpose. It is the `uv.lock` idea from Week 09, applied to a build
tool.

**The version is the tag.** `v0.1.0` becomes the package version and replaces
`{{version}}` in every `code.py`. Without a tag, builds are `0.0.0-dev.N`.

**While developing on a Mac with Rhino 8**, ghuser-builder's
`local/ghuser_dev.py --env src` builds without Docker and points each
component at your working copy of `src/`: edit the core, recompute in
Grasshopper. Development only; releases come from CI.

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
   This is the step you can safely delegate to an agent (Week 15): it is
   pure, and the tests are the reviewer that cannot be talked into approving.
3. **Review.** Read the code the agent wrote. Green tests prove it is
   *correct*; only you decide it is *good* — clear, no waste, sane names.
   Compare `src/compas_studio/wall.py` (reviewed) with `../wall.py` (raw model
   output) to see the gap tests do not catch.
4. **Adapter.** Add `components/Cs_NewThing/`: copy an existing one, keep
   the header, change the call and the conversion; a `metadata.json`, an icon.
5. **Ship.** Push (CI runs the tests, builds and verifies), then tag (CI
   releases the `.yak`).

The point of doing it this way is not that it is fast. It is that **you
understand and can vouch for every stage** — which is the only thing that lets
you use an AI to go faster without shipping something you cannot stand behind.
The lecture in `../README.md` walks through this loop in full.
