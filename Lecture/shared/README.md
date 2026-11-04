# What the notebooks share

[`viz.py`](viz.py) is the drawing helper every notebook imports, and
[`copy_to_mywork.py`](copy_to_mywork.py) copies notebooks into `MyWork/`
([how to run a notebook](../README.md#how-to-run-a-notebook)). The rest of this page is
for reference, and for the instructor.

## Three kinds of figure

| | **Drawn figures** (in the text) | **Diagrams** (`draw_mesh`, `draw_graph`, `chart` …, SVG) | **3D views** (`view3d`, compas_notebook) |
| --- | --- | --- | --- |
| what | designed explanations with labels and captions, made in advance by a week's `figures/make_figures.py` from real data | flat drawings of *your* data, made when you run a cell | interactive three.js: orbit, zoom |
| best for | the idea: what a halfedge is, what warp means | the result: which key is where, what a step did, a number over time | the geometry itself: a shell, a frame, a shape changing |
| you see it | as soon as the notebook opens, and on GitHub | after running the cell | after running the cell, in JupyterLab (verified) or VS Code (needs widget scripts) |

`compas_viewer` opens its own window and **does not render inside a notebook**.
**compas_notebook** draws with three.js in the page. `view3d()` in [`viz.py`](viz.py) wraps
it with two fixes:

- **Framing.** compas_notebook always looks at the origin from (0, −10, 5),
  with a far plane at 1000, so anything large or far from the origin starts
  off-screen, and a model in millimetres renders blank. `view3d` aims the
  camera at the bounding box of what you pass and scales the clipping planes.
- **Isolation.** compas_notebook's `Config` shares one view setting between all
  viewers by default; `view3d` gives each viewer its own.

```python
view3d(mesh)                                              # just look
view3d((mesh, {"facecolor": colours, "show_edges": True}),  # with options
       frame, (graph, {"nodesize": 0.2}))
```

**compas_timber models** have their own helper, `view_timber(model)`, because
they are in millimetres and benefit from shading. It draws straight with
pythreejs (what compas_notebook is built on): shaded beams, a one-metre grid,
and optionally the model graph inside them.

```python
view_timber(model, colors={"ridge": "#e8590c"})           # {beam name: colour}
view_timber(model, graph=True, opacity=0.2)               # a node per beam, an edge per joint
view_timber(model, stages={"sill_s": 0, "post_s0": 1})    # a slider that builds it stage by stage
explore_graph(model)                                      # pick a beam, see what it touches
```

Options are compas_notebook's, and not always compas_viewer's. Meshes take `facecolor`,
`show_edges`, `edgecolor`. Shapes such as `Box` take `color`; `surfacecolor` is silently
ignored. For hundreds of small pieces, build **one** mesh, not hundreds of shapes.

---

## For the instructor

```bash
uv run python -m pytest Lecture/shared -q                    # compas_timber notebooks are skipped
uv run --extra timber python -m pytest Lecture/shared -q     # everything
```

Edit the `.ipynb` directly, in JupyterLab. [`test_notebooks.py`](test_notebooks.py)
collects every `Lecture/Lecture_NN/notebooks/*.ipynb` and fails if one has outputs or
execution counts in it, if a picture its text points at is missing, if a
notebook sits outside a `notebooks/` folder or is missing from the README beside it, or if one no longer runs top to
bottom in a kernel.

To add a notebook: save it as `NN_name.ipynb` in its week's `notebooks/`
folder, give it the setup cell of its neighbours if it draws with `viz.py`,
and add a row to the README beside it.

**Pictures.** A *drawn figure* belongs to the week: add a function to that
week's `figures/make_figures.py` and show it in a markdown cell with
`![what it shows](../figures/name.svg)`. The *previews* in the notebook maps
are the notebooks' own output, saved to the week's `figures/` as `notebook-*.svg` by
[`make_previews.py`](make_previews.py) (add a line to `PICK`: the notebook, and a few
words from the title of the figure to show):

```bash
uv run Lecture/Lecture_05/figures/make_figures.py                  # Week 05's drawn figures
uv run --extra timber Lecture/shared/make_previews.py              # previews from notebook output
```
