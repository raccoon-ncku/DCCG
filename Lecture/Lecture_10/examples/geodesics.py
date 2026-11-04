"""Geodesic distance: Dijkstra along mesh edges vs the heat method (compas_cgal).

Edge paths can only turn at vertices, so they overestimate: on a quad grid
Dijkstra gives taxicab distance. W10 geometric README §3.
"""

import heapq


def edge_distances(mesh, source):
    """{vertex: shortest distance along edges from `source`} (Dijkstra)."""
    if not mesh.has_vertex(source):
        raise ValueError(f"no vertex {source!r}")
    dist = {source: 0.0}
    queue = [(0.0, source)]
    done = set()
    while queue:
        d, v = heapq.heappop(queue)
        if v in done:
            continue
        done.add(v)
        for n in mesh.vertex_neighbors(v):
            nd = d + mesh.edge_length((v, n))
            if nd < dist.get(n, float("inf")):
                dist[n] = nd
                heapq.heappush(queue, (nd, n))
    return dist


def heat_distances(mesh, source):
    """{vertex: geodesic distance} with the heat method (compas_cgal; triangles only)."""
    from compas_cgal.geodesics import heat_geodesic_distances

    keys = list(mesh.vertices())
    index = {k: i for i, k in enumerate(keys)}
    V = [mesh.vertex_coordinates(k) for k in keys]
    F = [[index[k] for k in mesh.face_vertices(f)] for f in mesh.faces()]
    d = heat_geodesic_distances((V, F), [index[source]])
    return {k: float(d[index[k]]) for k in keys}
