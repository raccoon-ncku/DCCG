"""Which streets carry the town? Edge betweenness on a street graph.

    uv run Lecture/Lecture_06/graph_applications/street_network.py

A grid split by a river with two bridges; networkx computes betweenness.
Graph.to_networkx() is directed: convert with .to_undirected().
W06 README §11.
"""

import networkx as nx
from compas.datastructures import Graph

RIVER_ROW = 3          # the river runs between street rows 3 and 4


def town(nx_cols=10, ny_rows=8, bridges=(2, 7)):
    """A street grid; north-south streets cross the river only at `bridges`."""
    graph = Graph()
    for j in range(ny_rows):
        for i in range(nx_cols):
            y = j + (0.6 if j > RIVER_ROW else 0.0)       # leave room for the river
            graph.add_node((i, j), x=float(i), y=y, z=0.0)
    for j in range(ny_rows):
        for i in range(nx_cols):
            if i + 1 < nx_cols:
                graph.add_edge((i, j), (i + 1, j), kind="street")
            if j + 1 < ny_rows:
                if j == RIVER_ROW and i not in bridges:
                    continue
                kind = "bridge" if j == RIVER_ROW else "street"
                graph.add_edge((i, j), (i, j + 1), kind=kind)
    return graph


def to_streets(graph):
    """The COMPAS graph as an UNDIRECTED networkx graph, with street lengths.

    Careful: graph.to_networkx() returns a DIRECTED graph (nx.DiGraph) --
    COMPAS stores each edge in the direction you added it (README section 2).
    Fed straight into networkx, every street becomes one-way, and half the
    town cannot reach the other half. .to_undirected() is the fix; the
    symptom, if you forget, is "Graph is not strongly connected" -- or worse,
    no error and quietly wrong numbers.
    """
    G = graph.to_networkx().to_undirected()
    for u, v in G.edges():
        G.edges[u, v]["length"] = graph.edge_length((u, v) if graph.has_edge((u, v)) else (v, u))
    return G


def street_betweenness(graph):
    """{edge: betweenness, 0..1}: share of shortest routes (by length) using each street."""
    G = to_streets(graph)
    eb = nx.edge_betweenness_centrality(G, weight="length", normalized=True)
    result = {}
    for (u, v), value in eb.items():
        result[(u, v) if graph.has_edge((u, v)) else (v, u)] = value
    return result


def average_trip(graph):
    """Mean shortest route length (m) over all pairs of corners."""
    return nx.average_shortest_path_length(to_streets(graph), weight="length")


if __name__ == "__main__":
    open_town = town()
    one_bridge = town(bridges=(7,))
    for name, g in (("both bridges open", open_town), ("west bridge closed", one_bridge)):
        eb = street_betweenness(g)
        busiest = max(eb, key=eb.get)
        print(f"{name:20s} busiest street {busiest} ({g.edge_attribute(busiest, 'kind')}), "
              f"share {eb[busiest]:.2f}; average trip {average_trip(g):.2f} blocks")
