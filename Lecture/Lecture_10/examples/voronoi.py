"""Delaunay triangulation and its dual, the Voronoi diagram.

Voronoi = the dual of the Delaunay mesh with vertices at circumcentres
instead of centroids. W10 geometric README §7.
"""

from compas.datastructures import Mesh
from compas.geometry import delaunay_triangulation


def delaunay(points):
    """A triangle Mesh of 2D points (z ignored and set to 0)."""
    pts = [[p[0], p[1], 0.0] for p in points]
    faces = [[int(i) for i in f] for f in delaunay_triangulation(pts)]
    mesh = Mesh.from_vertices_and_faces(pts, faces)
    mesh.unify_cycles()
    return mesh


def circumcentre(a, b, c):
    """Centre of the circle through three points in the XY plane."""
    d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    if abs(d) < 1e-12:
        raise ValueError("the three points are collinear")
    a2, b2, c2 = a[0] ** 2 + a[1] ** 2, b[0] ** 2 + b[1] ** 2, c[0] ** 2 + c[1] ** 2
    x = (a2 * (b[1] - c[1]) + b2 * (c[1] - a[1]) + c2 * (a[1] - b[1])) / d
    y = (a2 * (c[0] - b[0]) + b2 * (a[0] - c[0]) + c2 * (b[0] - a[0])) / d
    return [x, y, 0.0]


def voronoi_cells(mesh):
    """{interior vertex: its Voronoi cell, a list of points} from a Delaunay mesh.

    Boundary vertices have unbounded cells and are left out.
    """
    centre = {
        f: circumcentre(*(mesh.vertex_coordinates(v) for v in mesh.face_vertices(f)))
        for f in mesh.faces()
    }
    return {
        v: [centre[f] for f in mesh.vertex_faces(v, ordered=True)]
        for v in mesh.vertices()
        if not mesh.is_vertex_on_boundary(v)
    }
