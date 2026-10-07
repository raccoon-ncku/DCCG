# %% [markdown]
# # 09 · k-means on roof panels, by hand
#
# Companion to [W12 learning §1](../Algorithms/learning/README.md). 196 panels of
# a shallow roof, 49 distinct sizes. We run k-means one assign/update round at a
# time and watch the families form.

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
sys.path.insert(0, str(NB.parent / "Algorithms" / "learning" / "tutorials"))

import numpy as np  # noqa: E402

import kmeans as km  # noqa: E402

def show_clusters(X, labels, centres, title):
    colours = [["#1c7ed6", "#e8590c", "#2f9e44", "#7048e8", "#e03131", "#f59f00"][l % 6] for l in labels]
    return draw_points([list(x) for x in X] + [list(c) for c in centres], title,
                       colors=colours + ["#212529"] * len(centres), size=(300, 280))

# %% [markdown]
# ## Step 1 — the data: each panel as two numbers
# Width and depth in millimetres. Choosing these *features* is the modelling
# decision; the algorithm cannot tell whether they were the right ones.

# %%
X = km.roof_panels()
print(X.shape, "| width", X[:, 0].min().round(), "to", X[:, 0].max().round(), "mm")
print("distinct sizes:", len(np.unique(X.round(1), axis=0)))

# %% [markdown]
# ## Step 2 — three rounds of assign / update, by hand
# Assign every panel to its nearest centre; move every centre to the mean of
# its panels. Inertia (summed squared distance) can only go down.

# %%
k = 4
rng = np.random.default_rng(1)
centres = X[rng.choice(len(X), k, replace=False)]
figs = []
for r in range(3):
    d2 = ((X[:, None, :] - centres[None, :, :]) ** 2).sum(axis=2)
    labels = d2.argmin(axis=1)
    inertia = d2[np.arange(len(X)), labels].sum()
    print(f"round {r}: inertia {inertia:,.0f}, sizes {np.bincount(labels, minlength=k).tolist()}")
    figs.append(show_clusters(X, labels, centres, f"round {r}"))
    centres = np.array([X[labels == j].mean(axis=0) for j in range(k)])
row(*figs)

# %% [markdown]
# ## Step 3 — how many families for a tolerance?
# More clusters always fit better, so choose k by the fabricator's question:
# the smallest k whose worst panel is within tolerance.

# %%
for tol in (5, 10, 20):
    kk, (labels, centres, _, _) = km.families_needed(X, tolerance=tol, k_max=60)
    print(f"±{tol} mm -> {kk} families (worst deviation {km.worst_deviation(X, labels, centres):.1f} mm)")

# %% [markdown]
# ## Your turn
# 1. Start Step 2 from different random centres (`default_rng(5)`). Same result?
# 2. Add a third feature (panel twist). Does the family count at ±10 mm change?
