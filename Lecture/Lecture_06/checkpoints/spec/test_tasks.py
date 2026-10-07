# ──────────────────────────────────────────────────────────────────────────────
#  READ ONLY  ·  this file is the SPEC, not the answers.
#
#  Your work goes in  ../answers.py  (or ../answers_core.py + ../answers_runner.py
#  in Week 09). That file is auto-created from the shipped starter on first run
#  and is gitignored, so `git pull` never conflicts with it. Read the
#  assertions below to understand what each checkpoint is checking; do not
#  change them.
# ──────────────────────────────────────────────────────────────────────────────
"""
The SPECIFICATION for Week 06.

The apartment below is the one in the README figures. Most of these tests are
things you can check by looking at graph-plan.svg -- do that first; it is
faster than reading a failure.
"""

import math

import pytest
from compas.datastructures import Graph, Mesh

from answers import (
    accessible,
    dead_ends,
    hops_from,
    islands,
    mesh_to_graph,
    plan_graph,
    route,
)

# name: (x, y, area) -- the room centres from the README floor plan
ROOMS = {
    "entry": (1.5, 1.5, 9.0),
    "living": (6.0, 2.5, 30.0),
    "kitchen": (11.0, 2.5, 20.0),
    "hall": (1.5, 6.0, 18.0),
    "bed1": (5.0, 7.0, 16.0),
    "bath": (8.0, 7.0, 8.0),
    "bed2": (11.0, 7.0, 16.0),
}
DOORS = [
    ("entry", "living", 1.2),
    ("entry", "hall", 0.9),
    ("hall", "living", 0.9),
    ("living", "kitchen", 1.6),
    ("hall", "bed1", 0.8),
    ("living", "bath", 0.7),
    ("kitchen", "bed2", 0.8),
]


def apartment():
    return plan_graph(ROOMS, DOORS)


def corridor(n):
    """A straight row of n rooms, 1 m apart: r0 - r1 - ... - r(n-1)."""
    rooms = {f"r{i}": (float(i), 0.0, 1.0) for i in range(n)}
    doors = [(f"r{i}", f"r{i + 1}", 1.0) for i in range(n - 1)]
    return plan_graph(rooms, doors)


# --- 1. plan_graph ----------------------------------------------------------

def test_plan_has_a_node_per_room_and_an_edge_per_door():
    """7 rooms -> 7 nodes; 7 doors -> 7 edges"""
    graph = apartment()
    assert isinstance(graph, Graph)
    assert graph.number_of_nodes() == 7
    assert graph.number_of_edges() == 7


def test_plan_nodes_are_keyed_by_name():
    """node keys are the room names, not 0, 1, 2 ..."""
    assert set(apartment().nodes()) == set(ROOMS)


def test_plan_nodes_carry_position_and_area():
    """every node has x, y, z = 0 and an area"""
    graph = apartment()
    for name, (x, y, area) in ROOMS.items():
        assert graph.node_coordinates(name) == pytest.approx([x, y, 0.0])
        assert graph.node_attribute(name, "area") == pytest.approx(area)


def test_plan_edges_carry_the_door_width():
    """every door's width is stored on its edge, whichever way you ask"""
    graph = apartment()
    for a, b, width in DOORS:
        edge = (a, b) if graph.has_edge((a, b)) else (b, a)
        assert graph.has_edge(edge), f"no door between {a} and {b}"
        assert graph.edge_attribute(edge, "width") == pytest.approx(width)


def test_plan_rejects_a_door_to_nowhere():
    """a door that names an unknown room raises ValueError"""
    # Without this check, add_edge invents the room silently, with no
    # coordinates -- and the KeyError shows up later, far from the typo.
    with pytest.raises(ValueError):
        plan_graph(ROOMS, DOORS + [("hall", "atic", 0.8)])


# --- 2. dead_ends -----------------------------------------------------------

def test_dead_ends_are_the_rooms_with_one_door():
    """bed1, bath and bed2 each have exactly one door"""
    assert dead_ends(apartment()) == ["bath", "bed1", "bed2"]


def test_a_room_with_no_doors_is_not_a_dead_end():
    """degree 0 is unreachable, not a dead end -- the spec decides"""
    rooms = dict(ROOMS, store=(14.0, 1.0, 4.0))
    assert "store" not in dead_ends(plan_graph(rooms, DOORS))


# --- 3. hops_from -----------------------------------------------------------

def test_hops_counts_doors_from_the_entry():
    """entry 0; hall and living 1; bed1, bath, kitchen 2; bed2 3"""
    assert hops_from(apartment(), "entry") == {
        "entry": 0,
        "hall": 1,
        "living": 1,
        "bed1": 2,
        "bath": 2,
        "kitchen": 2,
        "bed2": 3,
    }


def test_hops_takes_the_shortest_count_around_a_loop():
    """entry -> hall -> living is a loop; living is still 1, not 2"""
    # A depth-first search would happily reach living via hall first and
    # record 2. Breadth-first records it at 1, because it finishes every room
    # one door away before looking two doors away.
    assert hops_from(apartment(), "hall")["living"] == 1


def test_hops_leaves_out_unreachable_rooms():
    """a room with no doors is simply absent from the result"""
    rooms = dict(ROOMS, store=(14.0, 1.0, 4.0))
    result = hops_from(plan_graph(rooms, DOORS), "entry")
    assert "store" not in result
    assert len(result) == 7


def test_hops_works_on_a_long_corridor():
    """the far end of a 30-room corridor is 29 doors away"""
    assert hops_from(corridor(30), "r0")["r29"] == 29


def test_hops_rejects_an_unknown_start():
    """starting from a room that does not exist raises ValueError"""
    with pytest.raises(ValueError):
        hops_from(apartment(), "garage")


# --- 4. route ---------------------------------------------------------------

def test_route_returns_the_rooms_and_the_length():
    """route(entry, bed2) goes through living and kitchen"""
    path, length = route(apartment(), "entry", "bed2")
    assert path == ["entry", "living", "kitchen", "bed2"]
    expected = (
        math.dist((1.5, 1.5), (6.0, 2.5))
        + math.dist((6.0, 2.5), (11.0, 2.5))
        + math.dist((11.0, 2.5), (11.0, 7.0))
    )
    assert length == pytest.approx(expected)


def test_route_prefers_short_over_few():
    """fewer doors is not the same as a shorter walk"""
    # Two ways from a to b: a long detour through ONE intermediate room
    # ("far", 5 m off to the side), or straight down a corridor of short
    # steps. Counting doors picks the detour. Measuring picks the corridor.
    rooms = {f"r{i}": (float(i), 0.0, 1.0) for i in range(6)}
    rooms["far"] = (2.5, 5.0, 1.0)
    doors = [(f"r{i}", f"r{i + 1}", 1.0) for i in range(5)]
    doors += [("r0", "far", 1.0), ("far", "r5", 1.0)]
    path, length = route(plan_graph(rooms, doors), "r0", "r5")
    assert path == ["r0", "r1", "r2", "r3", "r4", "r5"], (
        "this is the FEWEST-DOORS route. Which shortest_path did you call?"
        if path == ["r0", "far", "r5"]
        else f"unexpected route {path}"
    )
    assert length == pytest.approx(5.0)


def test_route_to_itself_is_free():
    """route(a, a) is ([a], 0.0)"""
    path, length = route(apartment(), "hall", "hall")
    assert path == ["hall"]
    assert length == pytest.approx(0.0)


def test_route_with_no_way_through_raises():
    """no route at all is a ValueError, not None"""
    rooms = dict(ROOMS, store=(14.0, 1.0, 4.0))
    with pytest.raises(ValueError):
        route(plan_graph(rooms, DOORS), "entry", "store")


# --- 5. accessible ----------------------------------------------------------

def test_accessible_drops_the_narrow_doors():
    """at 0.9 m, the three 0.8 m doors and the 0.7 m bath door go"""
    graph = accessible(apartment(), 0.9)
    assert graph.number_of_edges() == 4
    for u, v in graph.edges():
        assert graph.edge_attribute((u, v), "width") >= 0.9


def test_accessible_keeps_every_room():
    """rooms that lose all their doors are kept, with their attributes"""
    graph = accessible(apartment(), 0.9)
    assert set(graph.nodes()) == set(ROOMS)
    assert graph.node_attribute("bath", "area") == pytest.approx(8.0)
    assert graph.degree("bath") == 0


def test_accessible_does_not_touch_the_original():
    """the graph you were given is unchanged"""
    original = apartment()
    accessible(original, 2.0)
    assert original.number_of_edges() == 7


# --- 6. islands -------------------------------------------------------------

def test_one_island_when_everything_connects():
    """the apartment is one connected piece"""
    pieces = islands(apartment())
    assert pieces == [set(ROOMS)]


def test_islands_of_the_wheelchair_plan():
    """at 0.9 m the plan breaks into 4 pieces, the biggest first"""
    pieces = islands(accessible(apartment(), 0.9))
    assert len(pieces) == 4
    assert pieces[0] == {"entry", "hall", "living", "kitchen"}
    assert sorted(len(p) for p in pieces[1:]) == [1, 1, 1]
    assert set().union(*pieces) == set(ROOMS)


# --- 7. mesh_to_graph -------------------------------------------------------

def test_mesh_graph_has_the_same_vertices_and_edges():
    """nodes == vertices, edges == mesh edges, same keys, same positions"""
    mesh = Mesh.from_meshgrid(dx=4, nx=4, dy=3, ny=3)
    graph = mesh_to_graph(mesh)
    assert set(graph.nodes()) == set(mesh.vertices())
    assert graph.number_of_edges() == mesh.number_of_edges()
    for key in mesh.vertices():
        assert graph.node_coordinates(key) == pytest.approx(mesh.vertex_coordinates(key))
    for u, v in mesh.edges():
        assert graph.has_edge((u, v), directed=False)


def test_mesh_graph_answers_mesh_questions():
    """hops_from() on a mesh graph matches the mesh's own neighbours"""
    mesh = Mesh.from_meshgrid(dx=4, nx=4)
    graph = mesh_to_graph(mesh)
    hops = hops_from(graph, 12)
    assert {k for k, h in hops.items() if h == 1} == set(mesh.vertex_neighbors(12))
    assert hops[0] == 4     # corner to centre of a 4x4 grid: 2 across + 2 up
