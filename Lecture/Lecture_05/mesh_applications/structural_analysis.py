"""A triangulated mesh as a pin-jointed space truss (direct stiffness method).

    uv run Lecture/Lecture_05/mesh_applications/structural_analysis.py

Edges are bars, vertices are joints; one solve of K u = f gives every bar
force and joint displacement, stored back on the mesh as attributes. The demo
compares a hanging net, the inverted vault, and a pyramid that is a mechanism.
Triangulate first: quads shear. W05 README §12.
"""

import numpy as np


def analyse_truss(mesh, supports, load_per_area=-1.0, EA=1.0e4):
    """Analyse a triangulated mesh as a pin-jointed space truss.

    Parameters
    ----------
    mesh : Mesh -- triangulated; NOT modified
    supports : list[int] -- vertex keys pinned in x, y and z
    load_per_area : float -- vertical load, per unit of vertex area
    EA : float -- axial stiffness of every bar

    Returns
    -------
    Mesh -- a copy with
        edge attribute "force"          (+ tension, - compression)
        vertex attribute "displacement" ([dx, dy, dz])
    """
    if any(len(mesh.face_vertices(f)) != 3 for f in mesh.faces()):
        raise ValueError("triangulate first: quads are mechanisms in a pin-jointed truss")

    result = mesh.copy()
    keys = list(result.vertices())
    index = {key: i for i, key in enumerate(keys)}
    n = len(keys)
    X = np.array([result.vertex_coordinates(k) for k in keys])

    K = np.zeros((3 * n, 3 * n))
    bars = []
    for u, v in result.edges():
        i, j = index[u], index[v]
        d = X[j] - X[i]
        L = np.linalg.norm(d)
        e = d / L
        k = EA / L * np.outer(e, e)
        for a, b, sign in ((i, i, 1), (j, j, 1), (i, j, -1), (j, i, -1)):
            K[3 * a:3 * a + 3, 3 * b:3 * b + 3] += sign * k
        bars.append(((u, v), i, j, e, L))

    f = np.zeros(3 * n)
    for key in keys:
        f[3 * index[key] + 2] = load_per_area * result.vertex_area(key)

    pinned = set(supports)
    free = [3 * index[k] + c for k in keys if k not in pinned for c in range(3)]
    Kff = K[np.ix_(free, free)]
    if np.linalg.cond(Kff) > 1e12:
        # np.linalg.solve would still return numbers -- enormous, meaningless
        # ones. A solver that cannot fail loudly is not a verification tool.
        raise ValueError(
            "the truss is a mechanism: some joint can move without stretching "
            "any bar (flat regions, quads, or too few supports)"
        )
    u = np.zeros(3 * n)
    u[free] = np.linalg.solve(Kff, f[free])

    for (edge, i, j, e, L) in bars:
        stretch = e @ (u[3 * j:3 * j + 3] - u[3 * i:3 * i + 3])
        result.edge_attribute(edge, "force", float(EA / L * stretch))
    for key in keys:
        i = index[key]
        result.vertex_attribute(key, "displacement", [float(c) for c in u[3 * i:3 * i + 3]])
    return result


def tent(mesh, rise):
    """A pyramid over the same plan: flat facets meeting at a ridge. Returns a copy."""
    result = mesh.copy()
    xs, ys = result.vertices_attribute("x"), result.vertices_attribute("y")
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    half = (max(xs) - min(xs)) / 2
    for k in result.vertices():
        x, y, _ = result.vertex_coordinates(k)
        result.vertex_attribute(k, "z", rise * (1 - max(abs(x - cx), abs(y - cy)) / half))
    return result


def summary(mesh):
    forces = np.array(mesh.edges_attribute("force"))
    drift = max(np.linalg.norm(mesh.vertex_attribute(k, "displacement")) for k in mesh.vertices())
    return {
        "bars": len(forces),
        "compression_share": float(-forces[forces < 0].sum() / np.abs(forces).sum()),
        "max_tension": max(max(forces), 0.0),
        "max_compression": min(min(forces), 0.0),
        "max_displacement": float(drift),
    }


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent))
    from form_finding import edge_supported_net, form_find

    net, fixed = edge_supported_net()
    vault = form_find(net, fixed)
    shapes = {
        "hanging net": form_find(net, fixed, compression=False),
        "inverted vault": vault,
        "pyramid tent": tent(net, max(vault.vertices_attribute("z"))),
    }
    for name, shape in shapes.items():
        shape.quads_to_triangles()
        try:
            s = summary(analyse_truss(shape, fixed))
        except ValueError as error:
            print(f"{name:15s} {error}")
            continue
        print(f"{name:15s} compression share {s['compression_share']:5.1%}   "
              f"max tension {s['max_tension']:5.2f}   max compression {s['max_compression']:6.2f}   "
              f"max displacement {s['max_displacement']:.1e}")
