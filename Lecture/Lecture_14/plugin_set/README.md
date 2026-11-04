# compas_studio — a worked Grasshopper plugin set

The reference example for the software-engineering weeks: four components (a
running-bond wall, a staircase, a grid mesh, a stud wall) developed, tested and
built outside Rhino. Same shape as the [project template](/Lecture/Lecture_09/project_template/README.md).
The reasoning is in [Week 14](../README.md); this page is the map.

```
plugin_set/
├── pyproject.toml            what this is, which Python, which libraries
├── src/compas_studio/        1. CORE: pure Python + COMPAS, no Rhino
│   ├── wall.py               │   running_bond_wall()
│   ├── staircase.py          │   straight_staircase()
│   ├── grid.py               │   grid_mesh()
│   └── stud_wall.py          │   class StudWall
├── tests/                    2. SPEC: pytest, runs headless in CI
│   ├── test_wall.py, test_staircase.py, test_grid.py, test_stud_wall.py
│   └── test_components.py    │   every code.py agrees with its metadata.json
├── components/               3. ADAPTERS: one folder per GH component
│   ├── Cs_RunningBondWall/   │   code.py + metadata.json + icon.png
│   ├── Cs_Staircase/
│   ├── Cs_GridMesh/
│   └── Cs_StudWall/
├── yak.json + icon.png       the package's description in Rhino's Package Manager
├── scripts/ghuser            4. BUILD: components/ -> dist/, with ghuser-builder
└── .github/workflows/        5. PIPELINE
    ├── test.yml              │   every push: the tests (Linux, Python 3.9, no Rhino)
    └── build-ghuser.yml      │   every push: build + verify; every tag: release a .yak
```

**The rule:** the core knows nothing about Rhino, and components hold no logic.
Grep `src/` for `rhinoscriptsyntax` or `import Rhino`: nothing.

## Test

```bash
uv run pytest Lecture/Lecture_14/plugin_set/tests -q     # from the repo root: 32 passed
```

## Build

```bash
cd Lecture/Lecture_14/plugin_set
scripts/ghuser                                           # needs Docker
GHUSER_BUILDER_IMAGE=ghuser-builder:local scripts/ghuser # with an image you built yourself
ls dist dist/ghuser
```

It writes `dist/ghuser/Cs_*.ghuser` and `dist/compas-studio-<version>-rh8_0-any.yak`.
Drag the `.yak` onto Rhino 8. The core travels inside it (`lib/compas_studio`),
which is what the block at the top of every `code.py` looks for. A tag is a release:
`git tag v0.1.0 && git push --tags`.

## Add a component

1. **Spec:** `tests/test_newthing.py`, first.
2. **Core:** `src/compas_studio/newthing.py` until it passes. This is the step you
   can hand to an agent.
3. **Review:** green means correct; only you decide it is good. Compare
   `src/compas_studio/wall.py` (reviewed) with `../wall.py` (raw model output).
4. **Adapter:** copy a folder in `components/`, keep the header, change the class
   name, the call, the conversion, `metadata.json` and the 24 × 24 icon.
5. **Ship:** push (CI tests and builds), then tag (CI releases).
