# Exercises — Week 06 (Graphs)

> Open-ended graph practice. The [Week 06 checkpoints](/Lecture/Lecture_06/README.md#checkpoints)
> work on a fixed apartment with a checker; these ask you to model something
> of your own.
>
> They use the viewer, so run them locally: `uv run your_script.py`. If the
> viewer will not open on your machine, save the graph with
> `compas.json_dump` and print what you computed. The questions below are
> about numbers, not pictures.

## 1. A circulation graph of a real place

Pick a building you know: your home, the architecture building, a station.
Model it as a graph:

- a node per room or space, keyed by **name**, with `x, y, z` at its centre
  (use `z` for floors: a two-storey building is a 3D graph) and an `area`
- an edge per door, stair or opening, with a `width`, and a `kind`
  (`"door"`, `"stair"`, `"lift"`, `"opening"`)

Then answer, with code:

1. Which spaces are dead ends? Is that what you expected?
2. How many doors is the furthest room from the main entrance? Which room is it?
3. Keep only the edges a wheelchair can use (wide enough, and not `"stair"`).
   How many islands does the building break into? Which rooms are cut off?
4. Draw it: nodes coloured by hop count from the entrance, the inaccessible
   rooms in a different colour.

Your checkpoint functions do most of this already, and
[`plan_analysis.py`](/Lecture/Lecture_06/graph_applications/plan_analysis.py)
(README §11) does the rest for a gallery building: integration, escape
distance, critical doors. Copy what you need into your own script rather than
importing across folders, so that this exercise stands on its own. Then add one
question the script does not ask about *your* building.

> **Push it:** add a `"time"` attribute to each edge (seconds to walk it; a
> stair costs more than a corridor) and use `compas.topology.dijkstra_path`
> to find the *fastest* way out from every room. Which room has the longest
> escape time? That is the beginning of an egress analysis.

## 2. A timber frame of your own (compas_timber)

`uv sync --extra timber`, then start from
[`timber_frame.py`](/Lecture/Lecture_06/graph_applications/timber_frame.py).
Replace `stud_wall()` with something of yours: a roof truss, a pergola, a
reciprocal frame. Report how many L, T and X candidates the model finds.
Change `JOINT_RULE` (try `LMiterJoint`, `TTenonMortiseJoint`) and see how the
BTLx machining counts change. Which beam has the highest degree in
`model.graph`, and what does that mean on site?

## 3. An assembly sequence from a contact graph

Build a small brick wall (or a stack of any boxes) as a graph: one node per
brick, one edge per contact, as in README §8 and the notebook
[`04_bricks_and_mortar`](/Lecture/Lecture_06/notebooks/04_bricks_and_mortar.ipynb).

A brick can only be placed once everything it rests on is already there.
Starting from the bricks on the ground, find an order to place every brick in.

- Hint: it is a breadth-first search, but a brick only enters the queue when
  *all* of the bricks below it have been placed, not just one of them.
- Check your answer: for every brick, every brick below it must come earlier
  in the sequence. Write that check as a function that returns `True` or
  `False`. That is a test, and Week 10 is about exactly this.
- Animate it, or colour the bricks by their position in the sequence.

This is the core of how robotic assembly is planned, and a strong final-project
direction.

## 4. A mesh, seen as a graph

Take a mesh from Week 05, convert it with your `mesh_to_graph`, and run
`hops_from` from one vertex. Colour the **mesh** vertices by the hop count.

Now do the same with `graph.shortest_path` lengths instead of hop counts
(geodesic-ish distance along edges). Where do the two pictures differ, and why?
On a regular grid they look alike; on the Stanford bunny they do not.
