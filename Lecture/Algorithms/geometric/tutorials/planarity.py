"""Planar panels: measure flatness (diagonal distance / mean diagonal), then
planarize by projecting each face onto its best-fit plane and averaging.

The shape drifts in exchange for flatness; report both.
W10 geometric README §5.
"""

from compas.geometry import bestfit_plane


def flatness(mesh, face):
    """Distance between the diagonals of a quad / their mean length. Triangles: 0."""
    vs = mesh.face_vertices(face)
    if len(vs) == 3:
        return 0.0
    if len(vs) != 4:
        raise ValueError("flatness is defined here for triangles and quads only")
    a, b, c, d = (mesh.vertex_coordinates(v) for v in vs)
    return _segment_distance(a, c, b, d) / ((_dist(a, c) + _dist(b, d)) / 2)


def planarize(mesh, fixed=(), rounds=50):
    """Return a COPY of `mesh` with faces made (nearly) planar by projection."""
    result = mesh.copy()
    fixed = set(fixed)
    for _ in range(rounds):
        targets = {v: [] for v in result.vertices()}
        for f in result.faces():
            vs = result.face_vertices(f)
            origin, normal = bestfit_plane([result.vertex_coordinates(v) for v in vs])
            for v in vs:
                p = result.vertex_coordinates(v)
                d = sum((p[i] - origin[i]) * normal[i] for i in range(3))
                targets[v].append([p[i] - d * normal[i] for i in range(3)])
        for v, wanted in targets.items():
            if v in fixed or not wanted:
                continue
            result.vertex_attributes(v, "xyz", [sum(w[i] for w in wanted) / len(wanted) for i in range(3)])
    return result


def _dist(a, b):
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


def _segment_distance(p1, p2, q1, q2):
    """Closest distance between segments p1-p2 and q1-q2 (the two diagonals)."""
    u = [p2[i] - p1[i] for i in range(3)]
    v = [q2[i] - q1[i] for i in range(3)]
    w = [p1[i] - q1[i] for i in range(3)]
    a = sum(x * x for x in u)
    b = sum(u[i] * v[i] for i in range(3))
    c = sum(x * x for x in v)
    d = sum(u[i] * w[i] for i in range(3))
    e = sum(v[i] * w[i] for i in range(3))
    den = a * c - b * b
    s = 0.0 if den < 1e-12 else min(1.0, max(0.0, (b * e - c * d) / den))
    t = min(1.0, max(0.0, (b * s + e) / c))
    s = min(1.0, max(0.0, (b * t - d) / a))
    return _dist([p1[i] + s * u[i] for i in range(3)], [q1[i] + t * v[i] for i in range(3)])
