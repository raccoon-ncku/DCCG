"""Contour lines of a triangle mesh at height h.

Each crossed triangle gives one segment; segments are chained by the mesh edge
they cross (an integer key), not by matching float endpoints. Quads are
rejected: a saddle quad is ambiguous. W10 geometric README §6.
"""


def _crossing(mesh, u, v, h):
    a, b = mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)
    t = (h - a[2]) / (b[2] - a[2])
    return [a[i] + t * (b[i] - a[i]) for i in range(3)]


def contours(mesh, h):
    """Return the contour polylines of a TRIANGLE mesh at height h.

    Each polyline is a list of points; a closed one ends where it starts.
    """
    if any(len(mesh.face_vertices(f)) != 3 for f in mesh.faces()):
        raise ValueError("triangulate first (mesh.quads_to_triangles())")

    def above(v):
        return mesh.vertex_coordinates(v)[2] > h   # strictly: no vertex lies ON h

    def ekey(u, v):
        return (u, v) if u < v else (v, u)

    links = {}                                   # edge -> the edges it is joined to
    for f in mesh.faces():
        a, b, c = mesh.face_vertices(f)
        crossed = [ekey(u, v) for u, v in ((a, b), (b, c), (c, a)) if above(u) != above(v)]
        if len(crossed) == 2:
            e1, e2 = crossed
            links.setdefault(e1, []).append(e2)
            links.setdefault(e2, []).append(e1)

    def walk(start):
        """Follow links from `start` until an open end, or back to start."""
        chain, prev, cur = [start], None, start
        seen.add(start)
        while True:
            ahead = [e for e in links[cur] if e != prev]
            if not ahead:
                return chain                      # reached the mesh boundary
            nxt = ahead[0]
            if nxt == start:
                return chain + [start]            # a closed loop
            chain.append(nxt)
            seen.add(nxt)
            prev, cur = cur, nxt

    seen = set()
    polylines = []
    # open contours first, each walked from one of its two ends ...
    for e, nb in links.items():
        if len(nb) == 1 and e not in seen:
            polylines.append(walk(e))
    # ... then whatever is left is closed loops
    for e in links:
        if e not in seen:
            polylines.append(walk(e))
    return [[_crossing(mesh, u, v, h) for u, v in chain] for chain in polylines]
