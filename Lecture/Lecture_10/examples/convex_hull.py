"""Convex hull: the smallest convex shape around a set of points.

In 2D, Andrew's monotone chain: sort the points, walk left to right and back,
dropping every point that makes a right turn (one cross product). O(n log n),
all of it in the sort. In 3D, COMPAS's hull of a mesh's vertices gives its
collision mesh. W10 README §4.
"""

from compas.datastructures import Mesh
from compas.geometry import Box, Translation, dot_vectors, subtract_vectors
from compas.geometry import convex_hull as hull_faces


def cross(o, a, b):
    """z of (a - o) x (b - o). > 0: o->a->b turns left (counter-clockwise)."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    """Return the hull vertices, counter-clockwise, as a list of [x, y, 0].

    Collinear points on the hull's edges are left out: only the corners.
    Fewer than three distinct points cannot have a hull -- ValueError.
    """
    pts = sorted({(p[0], p[1]) for p in points})
    if len(pts) < 3:
        raise ValueError("a hull needs at least three distinct points")

    def half(seq):
        chain = []
        for p in seq:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], p) <= 0:
                chain.pop()                   # the middle point is not a corner
            chain.append(p)
        return chain

    lower = half(pts)
    upper = half(reversed(pts))
    hull = lower[:-1] + upper[:-1]            # each chain ends where the other starts
    if len(hull) < 3:
        raise ValueError("all points are collinear: there is no hull")
    return [[x, y, 0.0] for x, y in hull]


def area(polygon):
    """Signed area (shoelace formula). Positive for counter-clockwise."""
    n = len(polygon)
    return 0.5 * sum(polygon[i][0] * polygon[(i + 1) % n][1] - polygon[(i + 1) % n][0] * polygon[i][1]
                     for i in range(n))


def collision_mesh(mesh):
    """The convex hull of a mesh's vertices, as a closed mesh with outward faces."""
    points = [mesh.vertex_coordinates(v) for v in mesh.vertices()]
    faces = hull_faces(points)
    used = sorted({i for face in faces for i in face})
    index = {i: k for k, i in enumerate(used)}
    hull = Mesh.from_vertices_and_faces([points[i] for i in used], [[index[i] for i in face] for face in faces])
    hull.unify_cycles()
    if hull.volume() < 0:               # cycles unified, but pointing inward
        hull.flip_cycles()
    return hull


def inside(hull, point, tol=1e-9):
    """True if point is inside or on a convex mesh: behind the plane of every face."""
    return all(dot_vectors(subtract_vectors(point, hull.face_centroid(f)), hull.face_normal(f)) <= tol
               for f in hull.faces())


def corner_parts(length=0.6, size=0.12):
    """Three timber stubs meeting at a corner, one mesh each: a node a robot has to place."""
    half = length / 2
    stubs = [Box(length, size, size), Box(size, length, size), Box(size, size, length)]
    moves = [[half, 0, 0], [0, half, 0], [0, 0, half]]
    return [Mesh.from_shape(box).transformed(Translation.from_vector(move)) for box, move in zip(stubs, moves)]


def joined(parts):
    """All parts as one mesh."""
    whole = Mesh()
    for part in parts:
        whole.join(part)
    return whole
