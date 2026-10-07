# %% [markdown]
# # 06 · From Delaunay to Voronoi to Lloyd
#
# Companion to [W10 §7 and §10](../Algorithms/geometric/README.md). Scatter
# points, triangulate them, turn the triangles into Voronoi cells, then even the
# points out with Lloyd's algorithm, one round at a time.

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

import lloyd  # noqa: E402
import voronoi  # noqa: E402

# %% [markdown]
# ## Step 1 — scatter and triangulate

# %%
rnd = random.Random(11)
pts = [[rnd.uniform(0, 10), rnd.uniform(0, 6), 0] for _ in range(40)]
tri = voronoi.delaunay(pts)
print(tri.number_of_vertices(), "points ->", tri.number_of_faces(), "triangles")
draw_mesh(tri, "Delaunay triangulation", vertex_labels=False)

# %% [markdown]
# ## Step 2 — one triangle's circumcircle is empty
# Pick a triangle, compute the centre of the circle through its corners, and
# check no other point lies inside. That property *defines* Delaunay.

# %%
f = max(tri.faces(), key=tri.face_area)
corners = [tri.vertex_coordinates(v) for v in tri.face_vertices(f)]
centre = voronoi.circumcentre(*corners)
r = math.dist(centre, corners[0])
inside = [p for p in pts if math.dist(centre, p) < r - 1e-9]
print("radius", round(r, 2), "| points strictly inside:", len(inside))

# %% [markdown]
# ## Step 3 — Voronoi = the dual at circumcentres
# For each interior point, walk its triangles in order and join their
# circumcentres.

# %%
cells = voronoi.voronoi_cells(tri)
inner = [c for c in cells.values() if all(0 <= q[0] <= 10 and 0 <= q[1] <= 6 for q in c)]
print(len(cells), "bounded cells;", len(inner), "drawn (the rest reach past the frame)")
draw_points(pts, "Voronoi cells", polygons=inner, bounds=[[0, 0], [10, 6]])

# %% [markdown]
# ## Step 4 — Lloyd, round by round
# Move every point to the centroid of its (sampled) cell. Crowded points spread,
# gaps fill. The energy can only go down.

# %%
sites = [(p[0], p[1]) for p in pts]
samples = lloyd.samples(10, 6, 50)
snapshots, energies = [sites], [lloyd.energy(sites, samples)]
for _ in range(12):
    sites, hist = lloyd.lloyd(sites, samples, rounds=1)
    snapshots.append(sites)
    energies.append(hist[-1])
print("closest pair: before", round(min(lloyd.nearest_spacing(snapshots[0])), 2),
      "| after", round(min(lloyd.nearest_spacing(snapshots[-1])), 2))
row(draw_points(snapshots[0], "round 0", bounds=[[0, 0], [10, 6]], size=(300, 220)),
    draw_points(snapshots[3], "round 3", bounds=[[0, 0], [10, 6]], size=(300, 220)),
    draw_points(snapshots[12], "round 12", bounds=[[0, 0], [10, 6]], size=(300, 220)))

# %%
chart({"energy": energies}, "Lloyd energy, never increasing", "round")

# %% [markdown]
# ## Your turn
# 1. Restrict the samples to an L-shaped site with `lloyd.samples(..., inside=...)`.
# 2. Lloyd is k-means on a site. Open notebook 09 and find the two lines that
#    are the same.
