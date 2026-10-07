# Notebooks: mesh, graph and algorithms, step by step

The lectures explain; the tutorials are finished code. These notebooks sit in
between: they **unpack one idea at a time**, print every intermediate result,
and draw the data at each step, so you watch a mesh, a graph or an algorithm
being built rather than reading the result.

| # | Notebook | Companion to | What you watch happen |
| - | -------- | ------------ | --------------------- |
| 01 | [mesh from scratch](01_mesh_from_scratch.ipynb) | [W05](../Lecture_05/README.md) | keys, faces, halfedges, neighbours, the boundary trap, attributes, Euler catching a bug |
| 02 | [form finding](02_mesh_form_finding.ipynb) | [W05 §12](../Lecture_05/README.md#12-mesh-in-architecture-four-applications) | the force density method, one matrix at a time |
| 03 | [graph and BFS](03_graph_bfs_and_paths.ipynb) | [W06](../Lecture_06/README.md) | breadth-first search narrated step by step; the BFS tree; two `shortest_path`s disagreeing |
| 04 | [two graphs of one frame](04_graph_two_graphs.ipynb) | [W06 §3](../Lecture_06/README.md#3-a-mesh-is-a-graph) | joints found from centrelines; element graph vs bar graph |
| 05 | [curvature and smoothing](05_alg_curvature_smoothing.ipynb) | [W10](../Algorithms/geometric/README.md) | one angle defect by hand; Gauss–Bonnet; Laplacian shrinking vs Taubin |
| 06 | [Delaunay → Voronoi → Lloyd](06_alg_voronoi_lloyd.ipynb) | [W10](../Algorithms/geometric/README.md) | the empty circle; cells from circumcentres; Lloyd round by round |
| 07 | [cellular automata](07_sim_cellular_automata.ipynb) | [W11](../Algorithms/simulation/README.md) | neighbour counts as an array; the rule; a glider; a tower |
| 08 | [simulated annealing](08_opt_annealing.ipynb) | [W12](../Algorithms/optimization/README.md) | one move; the acceptance rule; why one run is an anecdote |
| 09 | [k-means by hand](09_learn_kmeans.ipynb) | [W12](../Algorithms/learning/README.md) | assign / update, round by round; families per tolerance |

Each notebook exists **twice**, with identical content:

- `NN_name.ipynb`: the notebook, for **Jupyter** and **VS Code**
- `NN_name.py`: the same cells as a plain script (`# %%` starts a cell), for
  **Zed**, which runs cells in `.py` files but does not open `.ipynb`

The `.py` is the source and the `.ipynb` is generated from it (see
*For the instructor* below).

---

## First, make your own copy

The files in this folder are updated by the instructor every week. **Do not
edit them in place**, or `git pull upstream main` will hit merge conflicts.
Copy the ones you want into `MyWork/`, which is yours
([MyWork/README.md](../../MyWork/README.md)):

```bash
uv run Lecture/notebooks/copy_to_mywork.py 03      # one notebook (both files)
uv run Lecture/notebooks/copy_to_mywork.py all     # all of them
```

The copies in `MyWork/notebooks/` still find the shared drawing helper
(`viz.py`), so they run exactly like the originals. It never overwrites a copy
you already have.

---

## Running them

`uv sync` installed everything: the kernel (`ipykernel`), **JupyterLab**, and
**compas_notebook** for 3D views (the project's `dev` group). Nothing else to
install.

### In your browser, with a small local server (recommended)

```bash
uv run jupyter lab Lecture/notebooks
```

This starts a **Jupyter server on your own laptop** and opens it in your
browser (`http://localhost:8888/lab?token=…`). Every figure works here: the
SVG diagrams and the interactive 3D views. Some things worth knowing:

- **It is local.** The server listens only on your machine (`localhost`),
  behind a one-time token in that URL. Nobody else can reach it, and nothing is
  uploaded anywhere.
- **The terminal is the server.** Keep it open while you work. Stop it with
  `Ctrl` + `C` (it asks to confirm; press `y` or `Ctrl` + `C` again). Closing
  the browser tab does *not* stop it.
- **Open a different folder** by changing the last argument, e.g.
  `uv run jupyter lab MyWork/notebooks` for your copies.
- **First time only**, JupyterLab asks *"Would you like to get notified about
  official Jupyter news?"*. Answer either way. If it ever asks you to
  *Select Kernel*, choose *Python 3 (ipykernel)*.
- **It reopens the tabs you had last time.** Add `?reset` to the URL for a
  clean window.
- **Run cells** with `Shift` + `Enter`, or *Run ▸ Run All Cells*.
- **It autosaves.** Saved outputs are not a problem in your `MyWork/` copies,
  because nbstripout keeps them out of commits (below).

This is exactly what the course tested: every notebook here, and the 3D
views, run in JupyterLab served this way.

### VS Code

1. Install the **Python** and **Jupyter** extensions (Microsoft).
2. Open the `.ipynb`.
3. *Select Kernel* (top right) ▸ *Python Environments* ▸ the one in this
   project's **`.venv`**. Not your system Python: it does not have COMPAS.
4. Run cells with `Shift` + `Enter`. SVG figures appear under the cells.
5. **3D views** are Jupyter *widgets*. VS Code loads the widget's JavaScript
   (three.js) from the internet the first time and may ask permission. If a 3D
   cell stays blank, allow it, or set `"jupyter.widgetScriptSources":
   ["jsdelivr.com", "unpkg.com"]` in VS Code's settings. If it still will not
   show, use the browser route above, which always works.

### Zed

Zed runs **`.py` files cell by cell** with its built-in REPL (Jupyter
kernels). It does not open `.ipynb`, and it cannot show widgets.

1. Open the **`.py`** twin, e.g. `MyWork/notebooks/03_graph_bfs_and_paths.py`.
2. Make sure Zed uses the project's `.venv` (it detects it when you open the
   repo folder; otherwise choose it in the kernel picker).
3. Put the cursor in a cell and run it with `repl: run`, `Ctrl` + `Shift` +
   `Enter` by default on macOS.
4. Text output appears inline. **3D cells print one line** telling you to use
   JupyterLab, because Zed has no widget support. **SVG figures**: if one does
   not render inline (support varies between Zed versions), end the cell with
   `fig.save("step.svg")` and open the file.

Zed is fine for stepping through the logic. For the pictures, use the browser.

---

## Two kinds of figure

| | **3D views** (`view3d`, compas_notebook) | **Diagrams** (`draw_mesh`, `draw_graph`, `chart` …, SVG) |
| --- | --- | --- |
| what | interactive three.js: orbit, zoom | flat drawings with **labels**: vertex keys, face keys, queue steps, charts |
| best for | the geometry itself: a shell, frames, a tower, a shape changing | the *structure*: which key is where, what a step did, a number over time |
| works in | JupyterLab (verified), VS Code (needs widget scripts) | everywhere: JupyterLab, VS Code, saved files |

`compas_viewer`, the desktop viewer used in the lecture scripts, opens its own
window and **does not render inside a notebook**. **compas_notebook** is the
COMPAS project's notebook viewer: the same `scene.add(...)` idea, drawn with
three.js in the page. `view3d()` in [`viz.py`](viz.py) wraps it with two
fixes that matter in class:

- **Framing.** compas_notebook always looks at the origin from (0, −10, 5),
  so anything large or far from the origin starts off-screen. `view3d` aims the
  camera at the bounding box of what you pass.
- **Isolation.** compas_notebook's `Config` shares one view setting between all
  viewers by default; `view3d` gives each viewer its own.

```python
view3d(mesh)                                              # just look
view3d((mesh, {"facecolor": colours, "show_edges": True}),  # with options
       frame, (graph, {"nodesize": 0.2}))
```

Options are compas_notebook's, and they are **not** always compas_viewer's.
Meshes take `facecolor` (one colour or `{face: colour}`), `show_edges`,
`edgecolor`. Shapes such as `Box` take `color`, not compas_viewer's
`surfacecolor`, which compas_notebook silently ignores (found the hard way:
every box came out black). For hundreds of small pieces, build **one** mesh,
not hundreds of shapes: notebook 07's tower does this, because hundreds of
boxes render slowly and one of them was drawn at the origin by mistake.

The older COMPAS-core notebooks (Week 04 `compas_ipynb/`, the Week 06 brick
stacks, Week 05 `mesh_pavilion.ipynb`) use compas_notebook directly, and now
run with the same `uv run jupyter lab`.

---

## Notebooks and git

A notebook file stores your code **and** every output you produced: numbers,
images, execution counts. Committed as-is, every run is a huge, unreadable
diff, and two people running the same notebook conflict. Three things keep this
repository clean.

**1. Install the output stripper, once per clone:**

```bash
uv run nbstripout --install
```

It registers a git *filter* in this clone. From then on, outputs are removed
**when you commit**, never from the file on your screen, so you keep seeing
your results. After you run a notebook, `git status` may still list it as
modified (git noticed the file was saved), but `git diff` shows nothing and
`git add` finds nothing to commit. Only real code changes get committed.

**2. Work in `MyWork/`, not here** (see above). Your copies, your history, no
conflicts with the instructor's updates.

**3. Prefer the `.py` for anything you want to diff or review.** It is plain
Python: `git diff` on it reads like any other code. That is also why it is the
source of truth here.

If you did edit a file in this folder by accident, put it back with
`git restore Lecture/notebooks/<file>`.

---

## For the instructor

```bash
uv run --with jupytext Lecture/notebooks/make_notebooks.py           # rebuild every .ipynb from its .py
uv run --with jupytext Lecture/notebooks/make_notebooks.py --check   # are they in sync?
uv run python -m pytest Lecture/notebooks -q                         # the guards below
```

Edit the `.py`, never the `.ipynb`. The generated notebooks have no outputs,
no execution counts and stable cell ids, so rebuilding an unchanged source
produces an identical file. [`test_notebooks.py`](test_notebooks.py) fails if
an `.ipynb` has outputs, if its code differs from its `.py` (someone edited the
generated file), or if any notebook no longer runs top to bottom.
