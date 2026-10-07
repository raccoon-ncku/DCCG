# %% [markdown]
# # 08 · Simulated annealing, one move at a time
#
# Companion to [W12 optimization §3](../Algorithms/optimization/README.md).
# Place 6 columns in an L-shaped plan so no point of the floor is far from a
# column. We look at the objective, make one move by hand, see why annealing
# sometimes accepts a *worse* move, then run it, and find out what a fair
# comparison needs.

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
sys.path.insert(0, str(NB.parent / "Algorithms" / "optimization" / "tutorials"))

import math  # noqa: E402
import random  # noqa: E402

import search  # noqa: E402

PLAN = [list(p) for p in search.PLAN]

def show_layout(layout, title, size=(320, 300)):
    return draw_points([list(p) for p in layout], title, polygons=[PLAN],
                       polygon_fills=["#f1f3f5"], bounds=PLAN, size=size)

# %% [markdown]
# ## Step 1 — the objective is one number
# The largest distance from any floor point to its nearest column.

# %%
rnd = random.Random(2)
layout = search.random_layout(6, rnd)
print("objective:", round(search.objective(layout), 2), "m")
show_layout(layout, "a random layout")

# %% [markdown]
# ## Step 2 — one move
# Nudge one column. Better or worse?

# %%
moved = search.nudge(layout, rnd, 1.5)
before, after = search.objective(layout), search.objective(moved)
print(f"before {before:.2f} m -> after {after:.2f} m:", "better" if after < before else "worse")

# %% [markdown]
# ## Step 3 — the acceptance rule
# Hill climbing only accepts better moves. Annealing accepts a worse move with
# probability exp(−Δ / T). Hot: almost always. Cold: almost never.

# %%
for delta in (0.05, 0.2, 0.5):
    print(f"worse by {delta} m:", "  ".join(f"T={t}: {math.exp(-delta / t):.2f}" for t in (1.0, 0.3, 0.1, 0.02)))

# %% [markdown]
# ## Step 4 — run both once, same budget
# Same start, same 1,500 evaluations. Look at who wins *this* run, and keep
# the result at arm's length.

# %%
_, hc_val, hc = search.hill_climb(budget=1500, seed=3)
_, sa_val, sa = search.simulated_annealing(budget=1500, seed=3)
print(f"seed 3: hill climbing {hc_val:.2f} m | annealing {sa_val:.2f} m")
chart({"hill climbing": hc[::10], "annealing": sa[::10]}, "best so far, one seed", "evaluations (×10)")

# %% [markdown]
# ## Step 5 — one run is an anecdote
# On seed 3, hill climbing happens to win. Run six seeds and compare the
# averages *and* the spreads. That is the only comparison worth reporting.

# %%
import statistics  # noqa: E402

seeds = range(6)
hc_runs = [search.hill_climb(budget=1500, seed=s)[1] for s in seeds]
sa_runs = [search.simulated_annealing(budget=1500, seed=s)[1] for s in seeds]
for name, runs in (("hill climbing", hc_runs), ("annealing", sa_runs)):
    print(f"{name:14s} mean {statistics.mean(runs):.2f} m, from {min(runs):.2f} to {max(runs):.2f}")

# %%
best_layout, best, _ = search.simulated_annealing(budget=1500, seed=0)
show_layout(best_layout, f"annealing, seed 0: worst point {best:.2f} m")

# %% [markdown]
# ## Your turn
# 1. Double the budget to 3,000. Does the gap between the means grow or shrink?
# 2. Set `t_start=0.001`. What has annealing become?
