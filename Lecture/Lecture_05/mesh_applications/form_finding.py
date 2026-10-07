"""Form finding with the force density method: a mesh as a cable net.

    uv run Lecture/Lecture_05/mesh_applications/form_finding.py

Fix some vertices, give each edge a force density q (an attribute), apply a
load, and one linear solve gives the equilibrium shape. Flipped, a hanging
net becomes a compression shell. W05 README §12.
"""

import numpy as np
from compas.datastructures import Mesh


def form_find(mesh, fixed, q=1.0, load=-0.25, compression=True):
    """Return a NEW mesh in equilibrium under a vertical load.

    Parameters
    ----------
    mesh : Mesh
        The starting net. Only its topology and the positions of the `fixed`
        vertices matter; the free vertices can start anywhere.
    fixed : list[int]
        Vertex keys that do not move (the supports).
    q : float
        Default force density for edges without a "q" attribute. Give edges
        their own "q" (mesh.edge_attribute(edge, "q", 5.0)) to stiffen them.
    load : float
        Vertical load per unit of vertex area. Negative = downwards.
    compression : bool
        True flips the hanging net upside down: tension -> compression.

    Returns
    -------
    Mesh -- a copy, with vertex coordinates in equilibrium and an edge
    attribute "force" (q * length; the sign says tension or compression).
    """
    result = mesh.copy()
    keys = list(result.vertices())
    index = {key: i for i, key in enumerate(keys)}
    edges = list(result.edges())
    fixed = set(fixed)
    free = [index[k] for k in keys if k not in fixed]
    supp = [index[k] for k in keys if k in fixed]
    if not supp:
        raise ValueError("a net with no fixed vertices has no equilibrium shape")

    # connectivity matrix: one row per edge, +1 at its start, -1 at its end
    C = np.zeros((len(edges), len(keys)))
    for row, (u, v) in enumerate(edges):
        C[row, index[u]] = 1.0
        C[row, index[v]] = -1.0
    Q = np.diag([result.edge_attribute(edge, "q") or q for edge in edges])

    X = np.array([result.vertex_coordinates(k) for k in keys])
    P = np.zeros_like(X)
    P[:, 2] = [load * result.vertex_area(k) for k in keys]

    Ci, Cf = C[:, free], C[:, supp]
    D = Ci.T @ Q @ Ci
    Df = Ci.T @ Q @ Cf
    X[free] = np.linalg.solve(D, P[free] - Df @ X[supp])

    if compression:
        X[:, 2] *= -1.0
    for key, (x, y, z) in zip(keys, X):
        result.vertex_attributes(key, "xyz", [float(x), float(y), float(z)])

    sign = -1.0 if compression else 1.0
    for edge in edges:
        qe = result.edge_attribute(edge, "q") or q
        result.edge_attribute(edge, "force", sign * qe * result.edge_length(edge))
    return result


def corner_supported_net(size=10.0, n=12, q_edge=6.0):
    """A square net held at its four corners, with stiffer boundary cables.

    Returns (mesh, fixed). The stiffer edges are what keep the free sides
    from collapsing inward: a designer's lever, set through an attribute.
    """
    mesh = Mesh.from_meshgrid(dx=size, nx=n)
    corners = [k for k in mesh.vertices() if mesh.vertex_degree(k) == 2]
    for edge in mesh.edges_on_boundary():
        mesh.edge_attribute(edge, "q", q_edge)
    return mesh, corners


def edge_supported_net(size=10.0, n=12):
    """A square net with its whole boundary fixed. Returns (mesh, fixed)."""
    mesh = Mesh.from_meshgrid(dx=size, nx=n)
    fixed = [k for k in mesh.vertices() if mesh.is_vertex_on_boundary(k)]
    return mesh, fixed


if __name__ == "__main__":
    mesh, fixed = corner_supported_net()
    shell = form_find(mesh, fixed)

    zs = shell.vertices_attribute("z")
    forces = shell.edges_attribute("force")
    print(f"vertices {shell.number_of_vertices()}, edges {shell.number_of_edges()}")
    print(f"rise: {max(zs):.2f} m over a {10.0:.0f} m span")
    print(f"edge forces: {min(forces):.2f} .. {max(forces):.2f}  (all negative = all compression)")

    from compas_viewer import Viewer

    viewer = Viewer()
    viewer.scene.add(shell, show_points=False)
    viewer.show()
