"""From a (simulated) LiDAR scan to a mesh, and back to the design.

    uv run Lecture/Lecture_05/mesh_applications/scan_to_mesh.py

scan -> drop outliers (KDTree) -> Delaunay in plan -> trim long-edged faces
(Euler checks the threshold) -> smooth heights -> deviation from design per
vertex. For full 3D scans see compas_cgal.reconstruction. W05 README §12.
"""

import math
import random

from compas.datastructures import Mesh
from compas.geometry import KDTree, delaunay_triangulation


def design_surface(x, y):
    """The surface the architect drew: a gently doubly-curved roof (m)."""
    return 1.2 + 0.6 * math.sin(math.pi * x / 10) * math.cos(math.pi * (y - 4) / 12) + 0.04 * x


def simulate_scan(n=900, noise=0.03, outliers=25, hole=(6.5, 4.0, 1.4), seed=1):
    """Return a list of [x, y, z] scan points over a 10 x 8 m roof."""
    rnd = random.Random(seed)
    hx, hy, hr = hole
    points = []
    while len(points) < n:
        x, y = rnd.uniform(0, 10), rnd.uniform(0, 8)
        if (x - hx) ** 2 + (y - hy) ** 2 < hr ** 2:
            continue                                  # occluded: a rooflight
        points.append([x, y, design_surface(x, y) + rnd.gauss(0, noise)])
    for _ in range(outliers):                         # birds, reflections
        x, y = rnd.uniform(0, 10), rnd.uniform(0, 8)
        points.append([x, y, design_surface(x, y) + rnd.choice([-1, 1]) * rnd.uniform(0.4, 1.5)])
    return points


def remove_outliers(points, k=8, tolerance=0.2):
    """Keep points whose height is close to the median of their k neighbours."""
    tree = KDTree(points)
    kept, dropped = [], []
    for p in points:
        nbrs = tree.nearest_neighbors(p, k + 1, distance_sort=True)[1:]
        zs = sorted(points[i][2] for _, i, _ in nbrs)
        median = zs[len(zs) // 2]
        (kept if abs(p[2] - median) < tolerance else dropped).append(p)
    return kept, dropped


def mesh_from_points(points, max_edge=1.4):
    """Triangulate in plan, then delete faces with an edge longer than max_edge.

    The Delaunay triangulation covers the convex hull, so it happily spans
    holes and concave edges with long thin triangles. Those are not surface:
    they are the absence of data, and leaving them in is how a scan model
    invents a roof over a rooflight.

    How long is too long? Euler (W05 section 8) answers it. This scan has ONE
    hole, so a correct mesh has V - E + F == 0. On the demo scan:

        max_edge   0.7   0.8   0.9   1.0   1.4
        euler      -16    -3    -2    -1     0

    Too strict, and the trim punches false holes wherever the scan happens
    to be sparse. One integer tells you, without looking.
    """
    faces = delaunay_triangulation(points)          # uses x, y; returns faces only
    mesh = Mesh.from_vertices_and_faces(points, [[int(i) for i in f] for f in faces])
    for f in list(mesh.faces()):
        cycle = mesh.face_vertices(f)
        if any(mesh.edge_length((u, v)) > max_edge for u, v in zip(cycle, cycle[1:] + cycle[:1])):
            mesh.delete_face(f)
    mesh.remove_unused_vertices()
    return mesh


def smooth_heights(mesh, rounds=2, weight=0.5):
    """Laplacian smoothing of z only, in place: noise goes down, shape stays."""
    for _ in range(rounds):
        new = {}
        for k in mesh.vertices():
            nbrs = mesh.vertex_neighbors(k)
            if not nbrs:
                continue
            avg = sum(mesh.vertex_attribute(n, "z") for n in nbrs) / len(nbrs)
            new[k] = (1 - weight) * mesh.vertex_attribute(k, "z") + weight * avg
        for k, z in new.items():
            mesh.vertex_attribute(k, "z", z)
    return mesh


def deviation(mesh, surface=design_surface):
    """Store "deviation" (scan minus design, m) on every vertex. Returns the mesh."""
    for k in mesh.vertices():
        x, y, z = mesh.vertex_coordinates(k)
        mesh.vertex_attribute(k, "deviation", z - surface(x, y))
    return mesh


def rms(values):
    values = list(values)
    return math.sqrt(sum(v * v for v in values) / len(values))


if __name__ == "__main__":
    raw = simulate_scan()
    clean, dropped = remove_outliers(raw)
    mesh = mesh_from_points(clean)
    before = rms(deviation(mesh).vertices_attribute("deviation"))
    smooth_heights(mesh)
    after = rms(deviation(mesh).vertices_attribute("deviation"))

    print(f"scan points      {len(raw)}  ({len(dropped)} dropped as outliers)")
    print(f"mesh             V={mesh.number_of_vertices()} F={mesh.number_of_faces()} "
          f"euler={mesh.euler()} (1 = a disc, 0 = one hole: the rooflight)")
    print(f"RMS deviation    {before * 1000:.0f} mm raw -> {after * 1000:.0f} mm smoothed")

    from compas.colors import Color
    from compas_viewer import Viewer

    worst = max(abs(d) for d in mesh.vertices_attribute("deviation"))
    colors = {k: Color.from_i(0.5 + 0.5 * mesh.vertex_attribute(k, "deviation") / worst)
              for k in mesh.vertices()}
    viewer = Viewer()
    viewer.scene.add(mesh, vertexcolor=colors, use_vertexcolors=True)
    viewer.show()
