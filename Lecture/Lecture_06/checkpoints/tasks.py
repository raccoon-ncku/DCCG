# STARTER FILE — READ ONLY.
#
# `checkpoints/conftest.py` copied me to  answers.py  on first run.
# Edit that file, not this one. If you delete answers.py, the next
# `uv run check.py NN` will regenerate it from this starter.

"""
Week 06 checkpoints — graphs: nodes, edges, and getting around.

Edit answers.py (copied from this starter). Run from the repository root:

    uv run check.py 06

The running example is a floor plan: ROOMS are nodes, DOORS are edges. It is
the same apartment as the figures in the README, so you can check most of
your answers by eye before you run the spec.

Still pure functions: data in, a graph or a plain value out. No viewer, no
files, no print.
"""

from collections import deque

from compas.datastructures import Graph


def plan_graph(rooms, doors):
    """Build a Graph of a floor plan.

    Parameters
    ----------
    rooms : dict[str, tuple[float, float, float]]
        room name -> (x, y, area). (x, y) is the centre of the room.
    doors : list[tuple[str, str, float]]
        (room_a, room_b, width) for every door.

    Rules
    -----
    - one node per room, KEYED BY ITS NAME ("kitchen", not 0, 1, 2 ...)
    - every node has x, y, z (z = 0) and an "area" attribute
    - one edge per door, with a "width" attribute
    - a door that mentions a room not in `rooms` is a mistake in the input:
      raise ValueError, naming the room

    Returns
    -------
    compas.datastructures.Graph

    Why the ValueError matters
    --------------------------
    graph.add_edge("hall", "atic") does NOT complain about the typo. It quietly
    creates a node called "atic" with no coordinates and no area -- and the
    crash happens much later, somewhere else, when something asks where
    "atic" is. Check at the boundary, where the mistake is still readable.

    Hint: graph.add_node(key, x=..., y=..., z=..., area=...) and
          graph.add_edge(u, v, width=...)
    """
    raise NotImplementedError("plan_graph")


def dead_ends(graph):
    """Return the rooms you can only enter one way, as a sorted list.

    A dead end has exactly ONE door. A room with no doors at all is not a dead
    end -- it is unreachable, which is a different (and worse) problem.

    Returns
    -------
    list -- node keys, sorted

    Hint: graph.degree(node)
    """
    raise NotImplementedError("dead_ends")


def hops_from(graph, start):
    """Return how many doors you pass through to reach each room from `start`.

    - {room: number of doors}; `start` itself is 0
    - rooms you cannot reach are NOT in the dictionary at all
    - a `start` that is not in the graph: raise ValueError

    Returns
    -------
    dict

    Write the breadth-first search yourself -- it is ten lines, and it is the
    single most useful algorithm on a graph. README section 5, and the
    "queue" recipe there.

    Hints
    -----
    - collections.deque is the queue: .append() on one end, .popleft() off
      the other
    - record a room's hop count the moment you FIRST see it, and never
      overwrite it. That one rule is what makes the answer the SHORTEST
      count, and what stops the search going round in circles.
    """
    raise NotImplementedError("hops_from")


def route(graph, start, goal):
    """Return the shortest WALKING route from `start` to `goal`.

    Walking distance is the sum of the straight-line distances between the
    centres of consecutive rooms (graph.edge_length does exactly that).

    Returns
    -------
    tuple[list, float] -- (the rooms in order, from start to goal; the total
    length). If start == goal: ([start], 0.0).

    If there is no route at all, raise ValueError.

    Watch out
    ---------
    COMPAS has TWO functions called shortest_path, and they answer different
    questions. One counts doors; the other measures distance. Read both
    docstrings (README section 6) before you trust either.
    """
    raise NotImplementedError("route")


def accessible(graph, min_width):
    """Return a NEW graph with only the doors at least `min_width` wide.

    - every room is kept, with all its attributes -- even a room that ends up
      with no doors. Dropping it would hide exactly the problem this function
      exists to find.
    - every door narrower than `min_width` is left out
    - the input graph must NOT be modified

    accessible(graph, 0.9) -> the plan as seen from a wheelchair

    Returns
    -------
    compas.datastructures.Graph

    Hint: graph.copy() gives you a full, independent copy. Or build a new
    graph and add what you keep -- both are fine. What is not fine is
    deleting edges from the graph you were given.
    """
    raise NotImplementedError("accessible")


def islands(graph):
    """Split the graph into its connected pieces.

    Returns
    -------
    list[set] -- one set of node keys per piece, LARGEST FIRST.

    A single room with no doors is a piece of its own.

    Combined with accessible(), this is a real design check: if
    islands(accessible(plan, 0.9)) has more than one piece, part of the
    building cannot be reached in a wheelchair.

    Hint: run your hops_from() from any room not yet assigned to a piece --
    everything it reaches is one piece. Repeat until every room is assigned.
    """
    raise NotImplementedError("islands")


def mesh_to_graph(mesh):
    """Return the graph of a mesh: its vertices and edges, without faces.

    - one node per vertex, with the SAME key and the same x, y, z
    - one edge per mesh edge

    Returns
    -------
    compas.datastructures.Graph

    After this, every function above works on a mesh too: hops_from() on a
    mesh is last week's vertex_ring(), from the other direction.
    """
    raise NotImplementedError("mesh_to_graph")
