"""Catmull-Clark subdivision, by hand: face points, edge points, moved vertices,
then n quads per n-gon.

Afterwards every face is a quad, V' = V + E + F, and Euler is unchanged; on a
closed mesh the result matches mesh.subdivided("catmullclark").
W10 geometric README §4.
"""

from compas.datastructures import Mesh


def catmull_clark(mesh):
    """Return a NEW mesh: one round of Catmull-Clark subdivision."""
    def P(v):
        return mesh.vertex_coordinates(v)

    def mean(points):
        return [sum(p[i] for p in points) / len(points) for i in range(3)]

    def ekey(u, v):
        return (u, v) if u < v else (v, u)

    face_point = {f: mean([P(v) for v in mesh.face_vertices(f)]) for f in mesh.faces()}

    edge_point = {}
    for u, v in mesh.edges():
        faces = [f for f in (mesh.halfedge_face((u, v)), mesh.halfedge_face((v, u))) if f is not None]
        if len(faces) == 2:
            edge_point[ekey(u, v)] = mean([P(u), P(v)] + [face_point[f] for f in faces])
        else:
            edge_point[ekey(u, v)] = mean([P(u), P(v)])

    vertex_point = {}
    for v in mesh.vertices():
        if mesh.is_vertex_on_boundary(v):
            nbrs = [n for n in mesh.vertex_neighbors(v) if mesh.is_edge_on_boundary((v, n))]
            p, a, b = P(v), P(nbrs[0]), P(nbrs[1])
            vertex_point[v] = [0.75 * p[i] + 0.125 * (a[i] + b[i]) for i in range(3)]
        else:
            n = mesh.vertex_degree(v)
            F = mean([face_point[f] for f in mesh.vertex_faces(v)])
            R = mean([mean([P(v), P(u)]) for u in mesh.vertex_neighbors(v)])
            p = P(v)
            vertex_point[v] = [(F[i] + 2 * R[i] + (n - 3) * p[i]) / n for i in range(3)]

    result = Mesh()
    vkey = {("v", v): result.add_vertex(x=x, y=y, z=z) for v, (x, y, z) in vertex_point.items()}
    vkey.update({("e", e): result.add_vertex(x=x, y=y, z=z) for e, (x, y, z) in edge_point.items()})
    vkey.update({("f", f): result.add_vertex(x=x, y=y, z=z) for f, (x, y, z) in face_point.items()})

    for f in mesh.faces():
        cycle = mesh.face_vertices(f)
        n = len(cycle)
        for i, v in enumerate(cycle):
            nxt, prv = cycle[(i + 1) % n], cycle[i - 1]
            result.add_face([
                vkey["v", v],
                vkey["e", ekey(v, nxt)],
                vkey["f", f],
                vkey["e", ekey(prv, v)],
            ])
    return result
