# Week 14 — Ship it: Grasshopper components with ghuser-builder

[`plugin_set/`](plugin_set/README.md) is the worked example: a plugin set developed, tested and shipped outside Rhino. Keep it open.

**How does pure Python geometry become something a colleague installs in
Grasshopper, without you ever pasting code into a component by hand?**

## 1. Grasshopper without `rhinoscriptsyntax`

Code typed into a GHPython node, reaching for `rhinoscriptsyntax`, only runs inside
a live Rhino document: it cannot be tested, versioned, or seen by CI or an agent.
COMPAS geometry is plain Python objects, so the core in `src/compas_studio/` runs
and is tested anywhere, and the component shrinks to an adapter: a fixed header
that finds the core, then a few lines that call it and convert with
`compas_rhino.conversions`. See
[`Cs_StudWall/code.py`](plugin_set/components/Cs_StudWall/code.py).

Each component is a folder of three files:

| File | Purpose |
| --- | --- |
| `code.py` | the adapter — a class with `RunScript(self, inputs...)` returning outputs |
| `metadata.json` | name, category, and the input/output parameters (names must match `code.py`) |
| `icon.png` | a 24×24 icon for the Grasshopper ribbon |

## 2. ghuser-builder: build, verify, package

You do **not need Rhino to build components**, nor Windows.
[**ghuser-builder**](https://git.rccn.dev/libs/ghuser-builder) is the lab's
tool for it: one Docker image with one command, `ghuser-build`.

```
components/                         ghuser-build                    dist/
├── Cs_RunningBondWall/             ─────────────►                  ├── ghuser/Cs_RunningBondWall.ghuser
│   ├── code.py                     1. componentize                 ├── ghuser/…
│   ├── metadata.json               2. verify: read every file back └── compas-studio-1.2.3-rh8_0-any.yak
│   └── icon.png  (24×24)           3. package as .yak
```

1. **Componentize.** The [COMPAS componentizer](https://github.com/compas-dev/compas-actions.ghpython_components)
   turns each folder into a `.ghuser` with `GH_IO.dll`, the library Grasshopper
   itself saves files with, on Mono, on Linux.
2. **Verify.** It opens every `.ghuser` again and checks the name, parameters and
   embedded code against your source. A mismatch fails the build. An artifact is
   evidence only after something has read it back. It does **not** compare
   `RunScript` with `metadata.json`; `tests/test_components.py` does that.
3. **Package.** The `.ghuser` files and your core go into one **`.yak`**, the file
   Rhino's Package Manager installs, updates and rolls back.

Three things that follow:

- **One build everywhere.** Your laptop and CI run the same image and command.
- **Pinned tools.** The image tag fixes the Grasshopper file library. A `.ghuser`
  written by a newer `GH_IO` than your user's Rhino will not load, so upgrading is
  a decision, like bumping `uv.lock`.
- **The version is the tag.** `git tag v1.2.3` is the only place it is written.
  `ghuser-build` puts it in the package name and replaces `{{version}}` in `code.py`.

## 3. Run it

**On your laptop** (needs Docker Desktop, OrbStack or colima):

```bash
cd Lecture/Lecture_14/plugin_set
scripts/ghuser                       # components/ -> dist/
ls dist dist/ghuser
```

[`scripts/ghuser`](plugin_set/scripts/ghuser) is one `docker run`, with this folder
mounted, calling `ghuser-build components dist`. If it says *no components
directory*, Docker cannot see the folder: keep the project under your home directory.

**In CI.** [`build-ghuser.yml`](plugin_set/.github/workflows/build-ghuser.yml)
runs the same image as the job's container and the same command, on every push.
The verifier compares each `.ghuser` with its source. It does not compare
`RunScript` with `metadata.json`: `tests/test_components.py` does that. A **tag**
also publishes:

```bash
git tag v0.1.0
git push --tags        # CI builds, verifies, and attaches the .yak to a GitHub Release
```

**On a Mac with Rhino 8, while developing** (no Docker): ghuser-builder's
`local/ghuser_dev.py` points each component at your working copy of `src/`, so you
edit the core and recompute in Grasshopper. Development only; see its README.

## 4. How the core gets into Rhino

A `.ghuser` holds only the adapter, so **Rhino has to find your core somewhere.**
ghuser-builder documents five ways. Two matter for you:

| | How the core travels | Users do | Use it when |
| --- | --- | --- | --- |
| **Vendored** (scenario D) | *inside* the `.yak`, in `lib/` | install one file | your core is pure Python: **the default in this course** |
| **Published** (scenario B) | on pypi.org; the adapter says `# r: my_core=={{version}}` | install the `.yak`; Rhino pip-installs the core on first run | the project is open source and others build on the library |

Vendoring is why every adapter starts with the same dozen lines: they find
`packages/<rhino>/compas-studio/<version>/lib` and put it on Python's path, so each
component loads the core of its own version. Public libraries such as COMPAS still
come from a `# r: compas` line, which Rhino resolves itself.

Two limits: the core must be pure Python, and after updating a package you
**restart Rhino**, because Python keeps the old module loaded.

## 5. Installing, and what a version means

A colleague drags the `.yak` onto a Rhino 8 window, and the components appear in
the Grasshopper ribbon under your `category`.

> ⚠️ **A placed component forgets where it came from.** A later release does
> **not** update instances already sitting in old `.gh` files. Version
> deliberately, and say what changed.

> ⚠️ **Status.** ghuser-builder's own README has a table of what has and has
> not been checked on a real Rhino. Read it before a deadline depends on it,
> and load your first `.yak` in Rhino early, not in Week 17.

## 6. The lighter path: JSON artifact + adapter

For a one-off, the artifact route is enough: dump a COMPAS JSON file and load it
with [`rhino_load.py`](/Lecture/Lecture_09/examples/rhino_load.py) in Rhino 8's ScriptEditor (`# r: compas`
installs COMPAS into Rhino's Python). `rhinomcp` also exposes the live document to
an agent as tools, which is good for sketching, but has no tests, no artifact and
no gate.
