# %% [markdown]
# # 03 · A floor plan as a graph, and breadth-first search by hand
#
# Companion to [Week 06](../Lecture_06/README.md). We build the apartment graph,
# then run breadth-first search one step at a time, printing the queue, so the
# algorithm stops being a black box.

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

from collections import deque  # noqa: E402

from compas.datastructures import Graph  # noqa: E402
from compas.topology import shortest_path  # noqa: E402

# %% [markdown]
# ## Step 1 — rooms are nodes, doors are edges
# Node keys are names. Every node gets `x, y, z` (its centre); every door a width.

# %%
rooms = {"entry": (1.5, 1.5), "living": (6.0, 2.5), "kitchen": (11.0, 2.5), "hall": (1.5, 6.0),
         "bed1": (5.0, 7.0), "bath": (8.0, 7.0), "bed2": (11.0, 7.0)}
doors = [("entry", "living", 1.2), ("entry", "hall", 0.9), ("hall", "living", 0.9),
         ("living", "kitchen", 1.6), ("hall", "bed1", 0.8), ("living", "bath", 0.7),
         ("kitchen", "bed2", 0.8)]

plan = Graph()
for name, (x, y) in rooms.items():
    plan.add_node(name, x=x, y=y, z=0)
for a, b, w in doors:
    plan.add_edge(a, b, width=w)
print(plan.number_of_nodes(), "rooms,", plan.number_of_edges(), "doors")
print("neighbours of living:", sorted(plan.neighbors("living")))
draw_graph(plan, "the apartment")

# %% [markdown]
# ## Step 2 — breadth-first search, narrated
# A queue of rooms to visit, oldest first, and a dictionary of hop counts that
# doubles as "already seen". Watch the queue: it always holds rooms at distance
# *d* before rooms at distance *d + 1*.

# %%
start = "entry"
hops = {start: 0}
parent = {start: None}
queue = deque([start])
step = 0
while queue:
    room = queue.popleft()
    new = []
    for nbr in sorted(plan.neighbors(room)):
        if nbr not in hops:
            hops[nbr] = hops[room] + 1
            parent[nbr] = room
            queue.append(nbr)
            new.append(nbr)
    step += 1
    print(f"step {step}: visit {room:8s} (hops {hops[room]})  found {new or '-'}  queue now {list(queue)}")

# %% [markdown]
# ## Step 3 — what the search produced
# Colour = hop count. The `parent` dictionary is a **tree**: 7 rooms, 6 edges.

# %%
top = max(hops.values())
print("hops:", hops)
print("parent:", parent)
draw_graph(plan, "hops from the entry", node_colors={n: ramp(h / top) for n, h in hops.items()})

# %% [markdown]
# ## Step 4 — the route itself, from the tree
# Follow `parent` back from the goal, then reverse.

# %%
goal = "bed2"
route = [goal]
while parent[route[-1]] is not None:
    route.append(parent[route[-1]])
route.reverse()
print("route:", " -> ".join(route))
draw_graph(plan, f"BFS route to {goal}", path=route)

# %% [markdown]
# ## Step 5 — two functions called shortest_path
# `compas.topology.shortest_path` counts **edges**. `Graph.shortest_path`
# measures **distance**. In this apartment they happen to agree, which is
# exactly why the difference is easy to miss. So test it where they cannot
# agree: a corridor of six rooms, plus one far-off room joined to both ends.

# %%
corridor = Graph()
for i in range(6):
    corridor.add_node(f"r{i}", x=float(i), y=0.0, z=0)
corridor.add_node("far", x=2.5, y=5.0, z=0)
for i in range(5):
    corridor.add_edge(f"r{i}", f"r{i + 1}")
corridor.add_edge("r0", "far")
corridor.add_edge("far", "r5")

def length(g, path):
    return sum(g.edge_length((a, b) if g.has_edge((a, b)) else (b, a)) for a, b in zip(path, path[1:]))

by_edges = shortest_path(corridor.adjacency, "r0", "r5")
by_length = corridor.shortest_path("r0", "r5")
print("fewest edges: ", by_edges, f"-> {len(by_edges) - 1} edges, {length(corridor, by_edges):.1f} m")
print("shortest walk:", by_length, f"-> {len(by_length) - 1} edges, {length(corridor, by_length):.1f} m")
row(draw_graph(corridor, "compas.topology.shortest_path", path=by_edges, size=(420, 300)),
    draw_graph(corridor, "graph.shortest_path", path=by_length, size=(420, 300)))

# %% [markdown]
# ## Your turn
# 1. Replace `popleft()` with `pop()` (a stack). Run Step 2 again: what changes
#    in the order, and are the hop counts still right?
# 2. Remove the hall–living door. Which hop counts change?
# 3. Keep only doors at least 0.9 m wide and run the search again. Which rooms
#    can a wheelchair not reach?
