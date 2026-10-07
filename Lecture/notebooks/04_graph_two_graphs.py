# %% [markdown]
# # 04 · Two graphs of one frame
#
# Companion to [Week 06 §3](../Lecture_06/README.md#3-a-mesh-is-a-graph). The
# same timber frame becomes two different graphs, depending on what a node
# *is*. Choosing between them is the abstraction step.

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

import math  # noqa: E402

from compas.datastructures import Graph  # noqa: E402

# %% [markdown]
# ## Step 1 — the frame as centrelines
# A portal frame: a beam, two posts, two knee braces. Plain line segments.

# %%
frame = {
    "beam": ((0, 3), (4, 3)),
    "post_L": ((0, 0), (0, 3)),
    "post_R": ((4, 0), (4, 3)),
    "knee_L": ((0, 1.8), (1.2, 3)),
    "knee_R": ((4, 1.8), (2.8, 3)),
}
draw_points([p for seg in frame.values() for p in seg], "five members",
            lines=list(frame.values()), labels=False)

# %% [markdown]
# ## Step 2 — where do members touch?
# A joint is where an **end** of one member lies on another. One cross product
# (is it on the line?) and one dot product (is it between the ends?).

# %%
def on_segment(p, a, b, tol=1e-9):
    cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    dot = (p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])
    return abs(cross) < tol and -tol <= dot <= math.dist(a, b) ** 2 + tol


joints = {}
names = list(frame)
for i, m in enumerate(names):
    for n in names[i + 1:]:
        for end in frame[m]:
            if on_segment(end, *frame[n]):
                joints[m, n] = end
        for end in frame[n]:
            if on_segment(end, *frame[m]):
                joints[m, n] = end
for (m, n), p in joints.items():
    print(f"{m:7s} meets {n:7s} at {p}")

# %% [markdown]
# ## Step 3 — the element graph: node = member, edge = joint
# This is how compas_timber, assembly planning and BTLx see a frame.

# %%
elements = Graph()
for name, (a, b) in frame.items():
    elements.add_node(name, x=(a[0] + b[0]) / 2, y=(a[1] + b[1]) / 2, z=0)
for (m, n), p in joints.items():
    elements.add_edge(m, n, at=p)
print("element graph:", elements.number_of_nodes(), "nodes,", elements.number_of_edges(), "edges")
print("degree:", {n: elements.degree(n) for n in elements.nodes()})
draw_graph(elements, "element graph")

# %% [markdown]
# ## Step 4 — the bar graph: node = point, edge = piece of member
# This is how structural analysis (Week 05's truss) sees the same frame. Each
# member is split at every joint along it.

# %%
points = []
for a, b in frame.values():
    for p in (a, b):
        if p not in points:
            points.append(p)
for p in joints.values():
    if p not in points:
        points.append(p)

bars = Graph()
for i, p in enumerate(points):
    bars.add_node(i, x=p[0], y=p[1], z=0)
for name, (a, b) in frame.items():
    along = sorted((i for i, p in enumerate(points) if on_segment(p, a, b)),
                   key=lambda i: math.dist(points[i], a))
    for u, v in zip(along, along[1:]):
        bars.add_edge(u, v, member=name)
print("bar graph:", bars.number_of_nodes(), "nodes,", bars.number_of_edges(), "edges")
row(draw_graph(elements, "node = member", size=(420, 320)),
    draw_graph(bars, "node = point", size=(420, 320)))

# %% [markdown]
# ### The frame in 3D
# The members as lines, the bar graph's nodes at the joints. Orbit it: the
# element graph has no place in 3D, because its nodes are *members*, not
# points. That is the difference in one picture.

# %%
from compas.geometry import Line  # noqa: E402

view3d(*[Line([a[0], 0, a[1]], [b[0], 0, b[1]]) for a, b in frame.values()],
       (bars, {"nodesize": 0.15}))

# %% [markdown]
# ## Your turn
# 1. Add a second beam at height 1.5 between the posts. Predict both graphs'
#    node and edge counts, then check.
# 2. Which graph would you use to answer "in what order can this be built?"
#    And "how much does the beam bend?" Why?
