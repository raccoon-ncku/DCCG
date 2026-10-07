# %% [markdown]
# # 07 · A cellular automaton, cell by cell
#
# Companion to [W11 simulation §1](../Algorithms/simulation/README.md). We count
# neighbours as an array, apply the rule, and watch a glider move, a shape that
# nobody wrote down.

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
sys.path.insert(0, str(NB.parent / "Algorithms" / "simulation" / "tutorials"))

import numpy as np  # noqa: E402

import cellular_automata as ca  # noqa: E402

def show_grid(grid, title):
    cells = [(x, -y) for y, x in zip(*np.nonzero(grid))]
    h, w = grid.shape
    squares = [[(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)] for x, y in cells]
    return draw_points([], title, polygons=squares, polygon_fills=["#1c7ed6"] * len(squares),
                       bounds=[[0, -h + 1], [w, 1]], size=(220, 220))

# %% [markdown]
# ## Step 1 — a glider, and its neighbour counts
# `neighbours()` adds eight shifted copies of the grid. Read the numbers: they
# decide who is born and who survives.

# %%
g = np.zeros((7, 7), bool)
g[1:4, 1:4] = ca.pattern([".#.", "..#", "###"])
print(g.astype(int))
print()
print(ca.neighbours(g))

# %% [markdown]
# ## Step 2 — apply B3/S23 once
# Born with exactly 3 neighbours; survive with 2 or 3.

# %%
n = ca.neighbours(g)
born = ~g & (n == 3)
survive = g & ((n == 2) | (n == 3))
nxt = born | survive
print("born:", int(born.sum()), "| survived:", int(survive.sum()), "| died:", int((g & ~survive).sum()))
print("same as ca.step:", bool((nxt == ca.step(g)).all()))

# %% [markdown]
# ## Step 3 — four generations
# After four steps the glider has the same shape, one cell down and right.

# %%
hist = ca.run(g, 4)
row(*[show_grid(h, f"gen {t}") for t, h in enumerate(hist)])

# %% [markdown]
# ## Step 4 — stack the generations into a tower
# Generation t becomes floor t. How many voxels does an R-pentomino make in 20
# floors?

# %%
seed = np.zeros((24, 24), bool)
seed[10:13, 10:13] = ca.pattern([".##", "##.", ".#."])
tower = ca.run(seed, 20)
print("population per floor:", [int(h.sum()) for h in tower])
print("voxels:", len(ca.voxels(tower)))
chart({"live cells": [int(h.sum()) for h in tower]}, "population per floor", "generation")

# %% [markdown]
# ### The tower in 3D
# Every live cell of every generation as a cube, floor by floor, built as
# **one** mesh (a single scene object draws much faster than hundreds of
# boxes), with each face coloured by its floor.

# %%
from compas.colors import Color  # noqa: E402
from compas.datastructures import Mesh  # noqa: E402

voxel_mesh, face_colors = Mesh(), {}
corners = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
sides = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
for x, y, z in ca.voxels(tower):
    keys = [voxel_mesh.add_vertex(x=x + dx, y=y + dy, z=z + dz) for dx, dy, dz in corners]
    for side in sides:
        face_colors[voxel_mesh.add_face([keys[i] for i in side])] = Color.from_i(z / len(tower))
print(voxel_mesh.number_of_faces(), "faces in one mesh")
view3d((voxel_mesh, {"facecolor": face_colors, "show_edges": True}))

# %% [markdown]
# ## Your turn
# 1. Change the rule to `born=(3, 6)` (HighLife). Does the glider survive?
# 2. Find a rule whose tower stays alive for 40 floors without filling the grid.
