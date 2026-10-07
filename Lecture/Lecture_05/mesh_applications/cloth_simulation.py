"""A cloth falling onto a sphere: position-based dynamics on a mesh.

    uv run Lecture/Lecture_05/mesh_applications/cloth_simulation.py

Vertices are particles, edges are length constraints; the mesh is copied to
numpy arrays for speed and back at the end. stretch() measures how far the
result is from the rest lengths. W05 README §12.
"""

import numpy as np
from compas.datastructures import Mesh


def cloth(size=4.0, n=24, height=1.6):
    """A flat square cloth, centred over the origin at `height`."""
    mesh = Mesh.from_meshgrid(dx=size, nx=n)
    for k in mesh.vertices():
        x, y, _ = mesh.vertex_coordinates(k)
        mesh.vertex_attributes(k, "xyz", [x - size / 2, y - size / 2, height])
    return mesh


def simulate(mesh, steps=240, dt=1 / 60, gravity=-9.81, iterations=25,
             sphere=((0.0, 0.0, 0.0), 1.0), ground=-0.6, pinned=(), damping=0.995,
             keep_every=None):
    """Drop `mesh` under gravity onto a sphere. Returns a NEW mesh.

    Parameters
    ----------
    pinned : keys of vertices that do not move (the corners of a curtain ...)
    keep_every : int or None
        If given, also return a list of frames (copies of the mesh) taken every
        `keep_every` steps -- for drawing the motion.

    Returns
    -------
    Mesh, or (Mesh, list[Mesh]) when keep_every is given
    """
    keys = list(mesh.vertices())
    index = {k: i for i, k in enumerate(keys)}
    X = np.array([mesh.vertex_coordinates(k) for k in keys], dtype=float)
    E = np.array([(index[u], index[v]) for u, v in mesh.edges()])
    rest = np.linalg.norm(X[E[:, 0]] - X[E[:, 1]], axis=1)
    free = np.ones(len(keys), dtype=bool)
    free[[index[k] for k in pinned]] = False
    centre, radius = np.array(sphere[0], dtype=float), sphere[1] * 1.02

    def to_mesh(P):
        result = mesh.copy()
        for k, (x, y, z) in zip(keys, P):
            result.vertex_attributes(k, "xyz", [float(x), float(y), float(z)])
        return result

    V = np.zeros_like(X)
    frames = []
    for step in range(steps):
        prev = X.copy()
        V[:, 2] += gravity * dt
        X[free] += damping * V[free] * dt

        for _ in range(iterations):
            d = X[E[:, 1]] - X[E[:, 0]]
            length = np.linalg.norm(d, axis=1)
            corr = (0.5 * (length - rest) / np.maximum(length, 1e-12))[:, None] * d
            delta = np.zeros_like(X)
            count = np.zeros(len(X))
            np.add.at(delta, E[:, 0], corr)
            np.add.at(delta, E[:, 1], -corr)
            np.add.at(count, E.ravel(), 1)
            # each vertex takes the AVERAGE of the corrections its edges ask
            # for, over-relaxed by 1.8 so the cloth converges in fewer passes
            X[free] += (1.8 * delta / np.maximum(count, 1)[:, None])[free]

            r = X - centre
            dist = np.linalg.norm(r, axis=1)
            inside = (dist < radius) & free
            X[inside] = centre + r[inside] / dist[inside, None] * radius
            X[:, 2] = np.where(free, np.maximum(X[:, 2], ground), X[:, 2])

        V = (X - prev) / dt
        if keep_every and step % keep_every == 0:
            frames.append(to_mesh(X))

    result = to_mesh(X)
    if keep_every:
        frames.append(result)
        return result, frames
    return result


def stretch(mesh, original):
    """Largest edge stretch, as a fraction of rest length. The honesty check.

    Real cloth barely stretches. A simulation that reports 15% has not
    converged (raise `iterations`); one that looks fine but was never measured
    is a picture, not a simulation. The demo settles at about 4%.
    """
    return max(
        abs(mesh.edge_length(e) / original.edge_length(e) - 1.0) for e in mesh.edges()
    )


if __name__ == "__main__":
    start = cloth()
    draped = simulate(start)
    zs = draped.vertices_attribute("z")
    print(f"vertices {draped.number_of_vertices()}, edges {draped.number_of_edges()}")
    print(f"z from {min(zs):.2f} to {max(zs):.2f}; worst edge stretch {stretch(draped, start):.1%}")
    print(f"topology unchanged: euler {start.euler()} -> {draped.euler()}")

    from compas_viewer import Viewer
    from compas.geometry import Sphere

    viewer = Viewer()
    viewer.scene.add(Sphere(radius=0.98))
    viewer.scene.add(draped)
    viewer.show()
