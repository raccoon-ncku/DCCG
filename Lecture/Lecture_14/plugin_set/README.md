# compas_studio — a worked Grasshopper plugin set

The reference example for the software-engineering weeks: four components (a
running-bond wall, a staircase, a grid mesh, a stud wall) developed, tested and
built outside Rhino. Same shape as [ghuser-template](https://github.com/rccn-dev/ghuser-template),
the template your project starts from.
The reasoning is in [Week 14](../README.md); this page is the map.

```
plugin_set/
├── pyproject.toml            what this is, which Python, which libraries; [tool.ghuser]
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
├── scripts/dev.py            4. DEV: components linked into Grasshopper, core read from src/
├── scripts/ghuser.py         5. SHIP: components/ -> dist/*.yak, core inside
└── .github/workflows/        6. PIPELINE
    ├── test.yml              │   every push: the tests (Linux, Python 3.9, no Rhino)
    └── build-ghuser.yml      │   every push: build + verify; every tag: release a .yak
```

**The rule:** the core knows nothing about Rhino, and components hold no logic.
Grep `src/` for `rhinoscriptsyntax` or `import Rhino`: nothing.

## Test

```bash
uv run pytest Lecture/Lecture_14/plugin_set/tests -q     # from the repo root: 36 passed
```

## Develop

```bash
uv run Lecture/Lecture_14/plugin_set/scripts/dev.py            # link into Grasshopper, reload Rhino
```

The components read the core from `src/`: edit it, run `dev.py` again, and the
canvas recomputes. After a `code.py` edit, replace that component; after a
`metadata.json` or icon edit, restart Rhino first. A component older than the build
stops and says so. `dev.py status` says what Grasshopper loads; `dev.py uninstall`
removes the link.

## Ship

```bash
uv run Lecture/Lecture_14/plugin_set/scripts/dev.py uninstall
uv run Lecture/Lecture_14/plugin_set/scripts/ghuser.py --version 0.1.0   # needs Docker
ls Lecture/Lecture_14/plugin_set/dist
```

It writes `dist/ghuser/Cs_*.ghuser` and `dist/compas-studio-0.1.0-rh8_0-any.yak`.
Drag the `.yak` onto Rhino 8 and restart it. The core travels inside it
(`lib/compas_studio`), which is what the block at the top of every `code.py` looks
for. A tag is a release: `git tag v0.1.0 && git push --tags`.

## Add a component

1. **Spec:** `tests/test_newthing.py`, first.
2. **Core:** `src/compas_studio/newthing.py` until it passes. This is the step you
   can hand to an agent.
3. **Review:** green means correct; only you decide it is good. Compare
   `src/compas_studio/wall.py` (reviewed) with `../wall.py` (raw model output).
4. **Adapter:** copy a folder in `components/`, keep the header, change the class
   name, the call, the conversion, `metadata.json` and the 24 × 24 icon. Run
   `dev.py` and restart Rhino to see it.
5. **Ship:** push (CI tests and builds), then tag (CI releases).
