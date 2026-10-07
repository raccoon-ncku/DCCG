# %% [markdown]
# # 01 · A mesh, step by step
#
# Companion to [Week 05](../Lecture_05/README.md). We build a mesh by hand, one
# call at a time, and *look* at what each call did. Run the cells in order.
#
# > Every figure here is drawn from the mesh data by `viz.py` (inline SVG).
# > `compas_viewer` opens a desktop window and does not render inside a
# > notebook, which is why it is not used here.

# %%
# Setup: run this cell first. It finds Lecture/notebooks/ (for viz.py) whether
# the kernel starts here (VS Code, Jupyter), at the repo root (Zed), or in your
# own copy under MyWork/, so the imports below work everywhere.
import sys
import pathlib

HERE = pathlib.Path.cwd()
NB = next(p / "Lecture" / "notebooks" for p in [HERE, *HERE.parents]
          if (p / "Lecture" / "notebooks" / "viz.py").exists())
sys.path.insert(0, str(NB))
from viz import chart, draw_graph, draw_mesh, draw_points, ramp, row, view3d  # noqa: E402

from compas.datastructures import Mesh  # noqa: E402

# %% [markdown]
# ## Step 1 — vertices are keys
# `add_vertex` returns an integer **key**. Keep it: faces are built from keys,
# not from coordinates.

# %%
mesh = Mesh()
a = mesh.add_vertex(x=0, y=0, z=0)
b = mesh.add_vertex(x=1, y=0, z=0)
c = mesh.add_vertex(x=1, y=1, z=0)
d = mesh.add_vertex(x=0, y=1, z=0)
print("keys:", a, b, c, d)
print("number of vertices:", mesh.number_of_vertices(), "| faces:", mesh.number_of_faces())

# %% [markdown]
# ## Step 2 — a face is a cycle of keys
# The order is counter-clockwise seen from above, so the normal points up.

# %%
f = mesh.add_face([a, b, c, d])
print("face", f, "->", mesh.face_vertices(f))
print("normal:", mesh.face_normal(f))
draw_mesh(mesh, "one face", face_labels=True)

# %% [markdown]
# ## Step 3 — the halfedges
# Every edge is stored twice, once per direction, and each direction knows the
# face on its left. On the boundary that face is `None`.

# %%
for u in mesh.halfedge:
    print(u, "->", dict(mesh.halfedge[u]))
print("halfedge (0, 1) has face", mesh.halfedge_face((0, 1)))
print("halfedge (1, 0) has face", mesh.halfedge_face((1, 0)), "  <- outside: the boundary")

# %% [markdown]
# ## Step 4 — a grid, built with a dictionary
# The trick from checkpoint 1: remember which key sits at grid position
# `(i, j)`, then look the corners up. Neighbouring faces then **share** keys.

# %%
def grid(nx, ny):
    m = Mesh()
    key = {}
    for j in range(ny + 1):
        for i in range(nx + 1):
            key[i, j] = m.add_vertex(x=i, y=j, z=0)
    for j in range(ny):
        for i in range(nx):
            m.add_face([key[i, j], key[i + 1, j], key[i + 1, j + 1], key[i, j + 1]])
    return m


g = grid(4, 3)
print("V E F =", g.number_of_vertices(), g.number_of_edges(), g.number_of_faces())
draw_mesh(g, "grid(4, 3)", face_labels=True)

# %% [markdown]
# ## Step 5 — neighbours are lookups
# Pick a vertex in the middle and ask the mesh about it. No coordinates are
# compared anywhere.

# %%
v = 7
print("vertex_neighbors:", g.vertex_neighbors(v))
print("vertex_faces:    ", g.vertex_faces(v))
print("face_neighbors(5):", g.face_neighbors(5))
row(
    draw_mesh(g, "vertex_neighbors(7)", highlight_vertices=g.vertex_neighbors(v),
              highlight_edges=[(v, n) for n in g.vertex_neighbors(v)], size=(400, 320)),
    draw_mesh(g, "vertex_faces(7)", highlight_faces=g.vertex_faces(v), face_labels=True, size=(400, 320)),
)

# %% [markdown]
# ## Step 6 — the boundary, and a trap
# `vertices_on_boundary()` walks the boundary as a **closed loop**: the first
# vertex comes back at the end. Count it, and compare.

# %%
loop = g.vertices_on_boundary()
print("len(loop) =", len(loop), "| distinct =", len(set(loop)))
print("first and last:", loop[0], loop[-1])
draw_mesh(g, "boundary", highlight_vertices=set(loop), highlight_edges=g.edges_on_boundary())

# %% [markdown]
# ## Step 7 — attributes: data that lives on geometry
# `x`, `y`, `z` are attributes like any other. Moving a vertex is setting
# its `z`; no face is touched.

# %%
import math  # noqa: E402

for k in g.vertices():
    x, y, _ = g.vertex_coordinates(k)
    g.vertex_attribute(k, "z", 0.6 * math.sin(x * 1.2) * math.cos(y * 0.8))
    g.vertex_attribute(k, "is_support", g.is_vertex_on_boundary(k))

zs = g.vertices_attribute("z")
lo, hi = min(zs), max(zs)
colours = {f: ramp((sum(g.vertex_attribute(k, "z") for k in g.face_vertices(f)) / 4 - lo) / (hi - lo))
           for f in g.faces()}
print("vertex 7 now:", g.vertex_attributes(7))
print("supports:", sorted(g.vertices_where(is_support=True)))
draw_mesh(g, "deformed, coloured by height", view="iso", vertex_labels=False, face_colors=colours)

# %% [markdown]
# ### The same mesh in 3D
# Drag to orbit, scroll to zoom. The colours are the face attribute dictionary
# you just filled in, handed to the viewer. (3D views need JupyterLab or VS
# Code; see the README.)

# %%
from compas.colors import Color  # noqa: E402

view3d((g, {"facecolor": {f: Color.from_hex(c) for f, c in colours.items()}, "show_edges": True}))

# %% [markdown]
# ## Step 8 — Euler: one integer that catches topology bugs
# A flat disc-like grid gives `V - E + F = 1`, before and after deforming,
# because deforming does not touch topology. Now build two quads that only
# *look* joined, each with its own corner vertices.

# %%
print("grid euler:", g.euler())

bad = Mesh()
left = [bad.add_vertex(x=x, y=y, z=0) for x, y in [(0, 0), (1, 0), (1, 1), (0, 1)]]
right = [bad.add_vertex(x=x, y=y, z=0) for x, y in [(1, 0), (2, 0), (2, 1), (1, 1)]]
bad.add_face(left)
bad.add_face(right)
print("two quads with duplicated vertices: euler =", bad.euler(), "(a 2x1 grid should give 1)")
row(draw_mesh(grid(2, 1), "shared vertices: euler 1", size=(400, 260)),
    draw_mesh(bad, "duplicated vertices: euler 2", size=(400, 260)))

# %% [markdown]
# ## Your turn
# 1. Build `grid(3, 3)` but wind one face clockwise. Which test from Step 2
#    shows it?
# 2. Delete the middle face of `grid(3, 3)` with `delete_face`. Predict the
#    Euler characteristic, then check.
# 3. Tag the four corners with `is_corner=True` and query them back with
#    `vertices_where`.
