# %% [markdown]
# # 05 · Curvature and smoothing, unpacked
#
# Companion to [W10 geometric algorithms §1–2](../Algorithms/geometric/README.md).
# We compute one angle defect by hand, check Gauss–Bonnet on a whole sphere,
# then watch Laplacian smoothing shrink a shape round by round.

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
sys.path.insert(0, str(NB.parent / "Algorithms" / "geometric" / "tutorials"))

import math  # noqa: E402
import random  # noqa: E402

from compas.datastructures import Mesh  # noqa: E402
from compas.geometry import Sphere  # noqa: E402

import curvature  # noqa: E402
import smoothing  # noqa: E402

# %% [markdown]
# ## Step 1 — the angles around one vertex
# On a flat sheet they add up to 360°. Lift the middle vertex of a grid and see
# what happens to the sum.

# %%
tent = Mesh.from_meshgrid(dx=2, nx=2)
mid = next(v for v in tent.vertices() if not tent.is_vertex_on_boundary(v))
tent.vertex_attribute(mid, "z", 0.6)
angles = [math.degrees(curvature.face_angle(tent, f, mid)) for f in tent.vertex_faces(mid)]
print("face angles at the peak:", [round(a, 1) for a in angles])
print("sum:", round(sum(angles), 1), "deg  -> angle defect:", round(360 - sum(angles), 1), "deg")
draw_mesh(tent, "a lifted vertex", view="iso", highlight_vertices=[mid])

# %% [markdown]
# ## Step 2 — Gauss–Bonnet, on a whole sphere
# Add the defects of every vertex of any closed mesh: you get 2π × Euler, which
# is 4π for anything sphere-like, whatever its shape.

# %%
ball = Mesh.from_shape(Sphere(radius=1.0), u=24, v=16)
total = curvature.total_curvature(ball)
print("sum of angle defects / pi =", round(total / math.pi, 6), "| euler =", ball.euler())

# %% [markdown]
# ## Step 3 — one Laplacian step, by hand
# Each vertex moves halfway toward the average of its neighbours. Compute all
# new positions first, *then* write them.

# %%
rnd = random.Random(0)
rough = ball.copy()
for v in rough.vertices():
    x, y, z = rough.vertex_coordinates(v)
    rough.vertex_attributes(v, "xyz", [x + rnd.uniform(-.06, .06), y + rnd.uniform(-.06, .06), z + rnd.uniform(-.06, .06)])

def mean_radius(m):
    return sum(math.dist(m.vertex_coordinates(v), (0, 0, 0)) for v in m.vertices()) / m.number_of_vertices()

new = {}
for v in rough.vertices():
    nbrs = rough.vertex_neighbors(v)
    c = [sum(rough.vertex_coordinates(n)[i] for n in nbrs) / len(nbrs) for i in range(3)]
    p = rough.vertex_coordinates(v)
    new[v] = [p[i] + 0.5 * (c[i] - p[i]) for i in range(3)]
print("before: radius", round(mean_radius(rough), 4), "roughness", round(smoothing.roughness(rough), 4))
for v, xyz in new.items():
    rough.vertex_attributes(v, "xyz", xyz)
print("after one step: radius", round(mean_radius(rough), 4), "roughness", round(smoothing.roughness(rough), 4))

# %% [markdown]
# ## Step 4 — thirty rounds: Laplacian shrinks, Taubin does not
# The tested module, round by round. Watch the radius.

# %%
start = ball.copy()
rnd = random.Random(0)
for v in start.vertices():
    x, y, z = start.vertex_coordinates(v)
    start.vertex_attributes(v, "xyz", [x + rnd.uniform(-.06, .06), y + rnd.uniform(-.06, .06), z + rnd.uniform(-.06, .06)])
lap = [mean_radius(smoothing.laplacian_smooth(start, rounds=r)) for r in range(0, 31, 3)]
tau = [mean_radius(smoothing.taubin_smooth(start, rounds=r)) for r in range(0, 31, 3)]
print("Laplacian:", round(lap[-1], 3), "| Taubin:", round(tau[-1], 3))
chart({"Laplacian": lap, "Taubin": tau}, "mean radius over 30 rounds", "rounds (×3)")

# %% [markdown]
# ### See the shrinking
# Noisy input, Laplacian after 30 rounds, Taubin after 30 rounds, side by side.

# %%
from compas.colors import Color  # noqa: E402
from compas.geometry import Translation  # noqa: E402

view3d((start, {"facecolor": Color.grey().lightened(50)}),
       (smoothing.laplacian_smooth(start, rounds=30).transformed(Translation.from_vector([2.5, 0, 0])),
        {"facecolor": Color.from_hex("#ffa8a8")}),
       (smoothing.taubin_smooth(start, rounds=30).transformed(Translation.from_vector([5, 0, 0])),
        {"facecolor": Color.from_hex("#74c0fc")}))

# %% [markdown]
# ## Your turn
# 1. In Step 3, update each vertex in place instead of collecting `new` first.
#    Does the result change? Why?
# 2. Try `taubin_smooth(..., mu=-0.5)`. What does the module say, and why?
