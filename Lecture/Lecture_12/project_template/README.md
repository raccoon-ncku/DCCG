# my_tool

One sentence: what this tool makes, and for whom.

> This is the **project template** from DCCG [Lecture 12, Part C](../README.md#part-c--scaffolding-a-project-week-13).
> Copy the folder out of the course repo, rename the four things below, and
> delete this note.

## Layout

```
my_tool/
├── pyproject.toml            name, version, Python, dependencies
├── src/my_tool/              1. CORE     pure Python + COMPAS. No Rhino in here
├── tests/                    2. SPEC     pytest. What "correct" means
├── components/Mt_*/          3. ADAPTERS one folder per Grasshopper component
│   ├── code.py               │           find the core, call it, convert
│   ├── metadata.json         │           name, inputs, outputs
│   └── icon.png              │           24 x 24
├── yak.json                  the package's description in Rhino's Package Manager
├── scripts/ghuser            4. BUILD    components/ -> dist/, with ghuser-builder
└── .github/workflows/        5. PIPELINE test.yml on every push; build-ghuser.yml builds, and releases on a tag
```

The rule that holds it together: **`src/` never imports Rhino, and
`components/` never contains logic.**

## Make it yours: rename four things

| What | Where | Example |
| --- | --- | --- |
| the Python package | the folder `src/my_tool/`, `pyproject.toml` (`name`, `packages`), the imports in `tests/` and `components/*/code.py` | `canopy_kit` |
| the Rhino package | `PACKAGE` in every `code.py`, `GHUSER_YAK_NAME` and `GHUSER_YAK_INCLUDE` in `scripts/ghuser` and `build-ghuser.yml` | `canopy-kit` |
| the component prefix | the folder `components/Mt_ColumnGrid/` and the class name inside its `code.py` (they must match) | `Ck_` |
| who and what | `yak.json`, `description` in `pyproject.toml`, `category` in each `metadata.json`, this README | |

Then check nothing was missed: `grep -rn "my_tool\|my-tool\|Mt_" .` should
print nothing.

## Work on it

```bash
uv sync                          # once: creates .venv with the core installed
uv run pytest                    # the spec. Run it after every change
uv run --python 3.9 pytest       # the same, on Rhino 8's Python: what CI runs
```

Add a function: write its test in `tests/` first, then the function in
`src/my_tool/`, then export it from `src/my_tool/__init__.py`.

## Build the Grasshopper components

```bash
scripts/ghuser                   # needs Docker; writes dist/ghuser/*.ghuser and dist/*.yak
```

Install the `.yak` by dragging it onto a Rhino 8 window. The core travels
inside it (`lib/my_tool`), so there is nothing else to set up.

To add a component: copy `components/Mt_ColumnGrid/` to a new folder, rename
the class to match the folder, change the one call and the conversion at the
bottom of `code.py`, and list the inputs and outputs in `metadata.json`. The
input names in `RunScript(self, ...)` must be the names in `metadata.json`.

## Release

```bash
git tag v0.1.0 && git push --tags
```

CI builds, verifies and attaches the `.yak` to a GitHub Release. The tag is
the version: it is written into the package and into every component.
