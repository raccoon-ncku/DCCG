"""Discrete Gaussian curvature: the angle defect, 2*pi minus the face angles at a
vertex (pi minus, on the boundary).

Free test, Gauss-Bonnet: the defects of a closed mesh sum to 2*pi * euler.
Only meaningful for planar faces: a ruled-hypar quad mesh shows zero
everywhere, so triangulate first. W10 geometric README §2.
"""

import math


def face_angle(mesh, face, vertex):
    """The interior angle of `face` at `vertex`, in radians."""
    cycle = mesh.face_vertices(face)
    i = cycle.index(vertex)
    a = mesh.vertex_coordinates(cycle[i - 1])
    b = mesh.vertex_coordinates(vertex)
    c = mesh.vertex_coordinates(cycle[(i + 1) % len(cycle)])
    u = [a[k] - b[k] for k in range(3)]
    w = [c[k] - b[k] for k in range(3)]
    dot = sum(u[k] * w[k] for k in range(3))
    nu = math.sqrt(sum(x * x for x in u))
    nw = math.sqrt(sum(x * x for x in w))
    return math.acos(max(-1.0, min(1.0, dot / (nu * nw))))


def angle_defect(mesh, vertex):
    """2*pi minus the angles around an interior vertex (pi minus, on the boundary)."""
    total = sum(face_angle(mesh, f, vertex) for f in mesh.vertex_faces(vertex))
    full = math.pi if mesh.is_vertex_on_boundary(vertex) else 2 * math.pi
    return full - total


def gaussian_curvature(mesh):
    """{vertex: angle defect / vertex area} -- curvature per unit area."""
    return {v: angle_defect(mesh, v) / mesh.vertex_area(v) for v in mesh.vertices()}


def total_curvature(mesh):
    """Sum of all angle defects. Gauss-Bonnet says: 2*pi * mesh.euler()."""
    return sum(angle_defect(mesh, v) for v in mesh.vertices())
