# %% [markdown]
# # 02 · Form finding, one matrix at a time
#
# Companion to [Week 05 §12](../Lecture_05/README.md#12-mesh-in-architecture-four-applications)
# and `Lecture_05/mesh_applications/form_finding.py`. Here the force density
# method is unpacked into its pieces, so you can see every array before it is
# used.

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

import numpy as np  # noqa: E402
from compas.datastructures import Mesh  # noqa: E402

# %% [markdown]
# ## Step 1 — a flat net with fixed corners
# A small grid keeps every matrix printable.

# %%
net = Mesh.from_meshgrid(dx=4, nx=4)
keys = list(net.vertices())
index = {k: i for i, k in enumerate(keys)}
edges = list(net.edges())
fixed = [k for k in keys if net.vertex_degree(k) == 2]          # the 4 corners
free = [index[k] for k in keys if k not in fixed]
supp = [index[k] for k in fixed]
print(len(keys), "vertices,", len(edges), "edges; fixed:", fixed)
draw_mesh(net, "the net; corners fixed", highlight_vertices=fixed)

# %% [markdown]
# ## Step 2 — the connectivity matrix C
# One row per edge, one column per vertex: `+1` at the edge's start, `-1` at
# its end. This matrix **is** the topology, written as numbers.

# %%
C = np.zeros((len(edges), len(keys)))
for row_, (u, v) in enumerate(edges):
    C[row_, index[u]] = 1
    C[row_, index[v]] = -1
print("C has shape", C.shape)
print(C[:5].astype(int))

# %% [markdown]
# ## Step 3 — force densities and loads
# `q` (force / length) is the designer's lever: one per edge. Stiffen the
# boundary edges and see what happens later.

# %%
q = np.array([6.0 if net.is_edge_on_boundary(e) else 1.0 for e in edges])
Q = np.diag(q)
P = np.zeros((len(keys), 3))
P[:, 2] = -0.25                                      # a vertical load on every vertex
print("q on boundary edges:", q[q > 1].size, "| interior:", q[q == 1].size)

# %% [markdown]
# ## Step 4 — one linear solve
# Split C into free and fixed columns and solve
# `(Ci^T Q Ci) X_free = P_free - (Ci^T Q Cf) X_fixed`.

# %%
X = np.array([net.vertex_coordinates(k) for k in keys])
Ci, Cf = C[:, free], C[:, supp]
D = Ci.T @ Q @ Ci
Df = Ci.T @ Q @ Cf
X[free] = np.linalg.solve(D, P[free] - Df @ X[supp])
X[:, 2] *= -1                                        # flip: hanging net -> standing shell
print("D is", D.shape, "| rise:", round(X[:, 2].max(), 2))

shell = net.copy()
for k, (x, y, z) in zip(keys, X):
    shell.vertex_attributes(k, "xyz", [float(x), float(y), float(z)])
row(draw_mesh(net, "before", view="iso", vertex_labels=False, size=(400, 320)),
    draw_mesh(shell, "after: a compression shell", view="iso", vertex_labels=False, size=(400, 320)))

# %% [markdown]
# ### Walk around the shell
# The flat net in grey, the found shell above it.

# %%
from compas.colors import Color  # noqa: E402
from compas.geometry import Translation  # noqa: E402

view3d((net, {"facecolor": Color.grey().lightened(60)}),
       (shell.transformed(Translation.from_vector([0, 0, 0.5])), {"facecolor": Color.from_hex("#74c0fc"), "show_edges": True}))

# %% [markdown]
# ## Step 5 — read the forces
# Force in each edge = q × length. All negative after the flip: compression.

# %%
lengths = np.linalg.norm(C @ X, axis=1)
forces = -q * lengths
print("force range:", forces.min().round(2), "to", forces.max().round(2))
print("topology unchanged:", net.euler(), "->", shell.euler())

# %% [markdown]
# ## Your turn
# 1. Set all `q` to 1. How do the free edges change in plan?
# 2. Fix the whole boundary instead of the corners. What shape do you get?
# 3. Compare with `form_find()` in `Lecture_05/mesh_applications/form_finding.py`:
#    which lines of this notebook does each of its lines correspond to?
