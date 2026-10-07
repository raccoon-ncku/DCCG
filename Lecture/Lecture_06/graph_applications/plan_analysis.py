"""A floor plan as a graph: integration, escape distance, critical doors.

    uv run Lecture/Lecture_06/graph_applications/plan_analysis.py

Integration: mean BFS depth per room (space syntax). Escape: one Dijkstra
started from all exits. Critical doors: edges whose removal splits the plan.
W06 README §11.
"""

import heapq
import math
from collections import deque

from compas.datastructures import Graph

ROOMS = {                           # name: (xmin, ymin, xmax, ymax), metres
    "lobby": (0, 0, 6, 6),
    "cafe": (6, 0, 12, 6),
    "shop": (12, 0, 16, 6),
    "office": (16, 0, 20, 6),
    "wc": (20, 0, 24, 3),
    "stair": (20, 3, 24, 6),
    "corr_w": (0, 6, 8, 8),
    "corr_m": (8, 6, 16, 8),
    "corr_e": (16, 6, 24, 8),
    "gallery1": (0, 8, 6, 16),
    "gallery2": (6, 8, 12, 16),
    "gallery3": (12, 8, 18, 16),
    "gallery4": (18, 8, 24, 16),
}
DOORS = [
    ("lobby", "cafe"), ("lobby", "corr_w"), ("cafe", "corr_m"),
    ("shop", "corr_m"), ("shop", "office"), ("office", "wc"),
    ("stair", "corr_e"), ("corr_w", "corr_m"), ("corr_m", "corr_e"),
    ("gallery1", "corr_w"), ("gallery2", "corr_m"), ("gallery3", "corr_m"),
    ("gallery4", "corr_e"),
    ("gallery1", "gallery2"), ("gallery2", "gallery3"), ("gallery3", "gallery4"),
]
EXITS = ["lobby", "stair"]


def door_point(a, b, rooms=ROOMS):
    """The middle of the wall that rooms a and b share."""
    ax0, ay0, ax1, ay1 = rooms[a]
    bx0, by0, bx1, by1 = rooms[b]
    x0, x1 = max(ax0, bx0), min(ax1, bx1)
    y0, y1 = max(ay0, by0), min(ay1, by1)
    if x0 > x1 or y0 > y1:
        raise ValueError(f"{a} and {b} do not share a wall")
    return [(x0 + x1) / 2, (y0 + y1) / 2, 0.0]


def plan_graph(rooms=ROOMS, doors=DOORS):
    """Rooms as nodes (at their centres), doors as edges.

    Each edge stores "length": centre -> door -> centre, the distance you
    actually walk, not the straight line through the wall.
    """
    graph = Graph()
    for name, (x0, y0, x1, y1) in rooms.items():
        graph.add_node(name, x=(x0 + x1) / 2, y=(y0 + y1) / 2, z=0.0,
                       area=(x1 - x0) * (y1 - y0))
    for a, b in doors:
        d = door_point(a, b, rooms)
        length = math.dist(graph.node_coordinates(a), d) + math.dist(d, graph.node_coordinates(b))
        graph.add_edge(a, b, door=d, length=length)
    return graph


def hops_from(graph, start):
    """Breadth-first search: {room: number of doors from start}."""
    hops = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nbr in graph.neighbors(node):
            if nbr not in hops:
                hops[nbr] = hops[node] + 1
                queue.append(nbr)
    return hops


def integration(graph):
    """{room: integration}. Higher = more integrated (shallower on average).

    mean depth  MD = sum of hops to every other room / (k - 1)
    relative asymmetry  RA = 2 (MD - 1) / (k - 2)     (0 .. 1)
    integration = 1 / RA

    Space syntax software usually normalises once more (RRA, by a "diamond"
    value for k), which matters when comparing different buildings. Within one
    plan, the ranking is what counts, and RA already gives it.
    """
    k = graph.number_of_nodes()
    result = {}
    for room in graph.nodes():
        hops = hops_from(graph, room)
        if len(hops) < k:
            raise ValueError(f"{room} cannot reach every room: integration is undefined")
        md = sum(hops.values()) / (k - 1)
        ra = 2 * (md - 1) / (k - 2)
        result[room] = 1 / ra if ra > 0 else float("inf")
    return result


def escape_distance(graph, exits=EXITS):
    """{room: metres to the nearest exit} -- Dijkstra from all exits at once."""
    dist = {e: 0.0 for e in exits}
    queue = [(0.0, e) for e in exits]
    done = set()
    while queue:
        d, room = heapq.heappop(queue)
        if room in done:
            continue
        done.add(room)
        for nbr in graph.neighbors(room):
            edge = (room, nbr) if graph.has_edge((room, nbr)) else (nbr, room)
            nd = d + graph.edge_attribute(edge, "length")
            if nd < dist.get(nbr, float("inf")):
                dist[nbr] = nd
                heapq.heappush(queue, (nd, nbr))
    return dist


def critical_doors(graph):
    """Doors whose removal splits the plan into more pieces (graph bridges)."""
    def pieces(g):
        seen, count = set(), 0
        for n in g.nodes():
            if n not in seen:
                seen |= set(hops_from(g, n))
                count += 1
        return count

    base = pieces(graph)
    critical = []
    for edge in list(graph.edges()):
        trial = graph.copy()
        trial.delete_edge(edge)
        if pieces(trial) > base:
            critical.append(edge)
    return critical


if __name__ == "__main__":
    graph = plan_graph()
    integ = integration(graph)
    escape = escape_distance(graph)

    print("most integrated:", ", ".join(sorted(integ, key=integ.get, reverse=True)[:3]))
    print("most segregated:", ", ".join(sorted(integ, key=integ.get)[:3]))
    limit = 25.0
    for room, d in sorted(escape.items(), key=lambda kv: -kv[1]):
        flag = "  <-- over the 25 m limit" if d > limit else ""
        print(f"  {room:9s} {d:5.1f} m to an exit{flag}")
    print("critical doors:", critical_doors(graph))
