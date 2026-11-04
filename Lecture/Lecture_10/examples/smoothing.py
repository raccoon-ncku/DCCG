"""Laplacian smoothing (shrinks a closed shape) and Taubin smoothing (does not).

Compute all new positions from the old ones before writing any.
W10 geometric README §1.
"""


def _step(mesh, fixed, w):
    new = {}
    for v in mesh.vertices():
        if v in fixed:
            continue
        nbrs = mesh.vertex_neighbors(v)
        if not nbrs:
            continue
        p = mesh.vertex_coordinates(v)
        c = [sum(mesh.vertex_coordinates(n)[i] for n in nbrs) / len(nbrs) for i in range(3)]
        new[v] = [p[i] + w * (c[i] - p[i]) for i in range(3)]
    for v, xyz in new.items():           # write AFTER reading everything
        mesh.vertex_attributes(v, "xyz", xyz)


def laplacian_smooth(mesh, fixed=(), rounds=10, weight=0.5):
    """Return a smoothed COPY of `mesh`. Vertices in `fixed` do not move."""
    result = mesh.copy()
    fixed = set(fixed)
    for _ in range(rounds):
        _step(result, fixed, weight)
    return result


def taubin_smooth(mesh, fixed=(), rounds=10, lam=0.5, mu=-0.53):
    """Return a smoothed COPY of `mesh` that (mostly) keeps its size."""
    if not (mu < -lam < 0):
        raise ValueError("Taubin needs mu < -lam < 0, e.g. lam=0.5, mu=-0.53")
    result = mesh.copy()
    fixed = set(fixed)
    for _ in range(rounds):
        _step(result, fixed, lam)
        _step(result, fixed, mu)
    return result


def roughness(mesh):
    """Mean length of the umbrella vector: 0 for a perfectly 'average' mesh."""
    total = 0.0
    for v in mesh.vertices():
        nbrs = mesh.vertex_neighbors(v)
        p = mesh.vertex_coordinates(v)
        c = [sum(mesh.vertex_coordinates(n)[i] for n in nbrs) / len(nbrs) for i in range(3)]
        total += sum((c[i] - p[i]) ** 2 for i in range(3)) ** 0.5
    return total / mesh.number_of_vertices()
