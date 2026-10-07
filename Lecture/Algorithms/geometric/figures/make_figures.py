"""
Draw every figure in the Geometric Algorithms README -- from the algorithms.

    uv run Lecture/Algorithms/geometric/figures/make_figures.py

Every picture calls the functions in ../tutorials (the same ones the tests
check), so a figure can never show something the code does not do.

The SVG-writing helpers are a copy of the ones in
Lecture/Lecture_05/figures/make_figures.py -- duplicated on purpose so each
folder stays runnable on its own.
"""

import math
import random
import sys
from pathlib import Path

from compas.datastructures import Mesh
from compas.geometry import Sphere, Torus

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "tutorials"))
import contouring  # noqa: E402
import convex_hull  # noqa: E402
import lloyd  # noqa: E402
import nearest  # noqa: E402
import curvature  # noqa: E402
import geodesics  # noqa: E402
import planarity  # noqa: E402
import smoothing  # noqa: E402
import subdivision  # noqa: E402
import voronoi  # noqa: E402

# ----------------------------------------------------------------------------
# palette
# ----------------------------------------------------------------------------
INK = "#212529"
GREY = "#adb5bd"
LIGHT = "#f1f3f5"
FACE = "#e7f5ff"
BLUE = "#1c7ed6"
ORANGE = "#e8590c"
GREEN = "#2f9e44"
RED = "#e03131"
PURPLE = "#7048e8"


# ----------------------------------------------------------------------------
# a very small SVG writer
# ----------------------------------------------------------------------------
class Figure:
    """An SVG canvas made of side-by-side panels."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.items = []

    def add(self, item):
        self.items.append(item)

    def save(self, name):
        body = "\n".join(self.items)
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" '
            f'height="{self.height}" viewBox="0 0 {self.width} {self.height}" '
            'font-family="Helvetica, Arial, sans-serif">\n'
            f'<rect width="100%" height="100%" fill="white"/>\n{body}\n</svg>\n'
        )
        (HERE / name).write_text(svg)
        print("wrote", name)


class Panel:
    """A rectangle on a Figure that maps world coordinates onto the page.

    view="plan" looks straight down (x right, y up). view="iso" is a simple
    isometric view, so z shows as height on the page.
    """

    def __init__(self, fig, x0, y0, w, h, points, view="plan", title=None, pad=34):
        self.fig = fig
        self.view = view
        if title:
            fig.add(_text(x0 + w / 2, y0 + 20, title, 15, INK, "middle", "bold"))
            y0 += 30
            h -= 30
        xy = [self._raw(p) for p in points]
        xs = [p[0] for p in xy]
        ys = [p[1] for p in xy]
        spanx = max(max(xs) - min(xs), 1e-9)
        spany = max(max(ys) - min(ys), 1e-9)
        self.s = min((w - 2 * pad) / spanx, (h - 2 * pad) / spany)
        cx = (max(xs) + min(xs)) / 2
        cy = (max(ys) + min(ys)) / 2
        self.ox = x0 + w / 2 - cx * self.s
        self.oy = y0 + h / 2 + cy * self.s

    def _raw(self, p):
        x, y = p[0], p[1]
        z = p[2] if len(p) > 2 else 0.0
        if self.view == "iso":
            c, s = math.cos(math.radians(30)), math.sin(math.radians(30))
            return ((x - y) * c, (x + y) * s + z)
        return (x, y)

    def map(self, p):
        X, Y = self._raw(p)
        return (self.ox + X * self.s, self.oy - Y * self.s)

    # drawing, in WORLD coordinates
    def line(self, a, b, color=INK, width=1.5, dash=None, opacity=1.0):
        (x1, y1), (x2, y2) = self.map(a), self.map(b)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.fig.add(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
            f'opacity="{opacity}"{d}/>'
        )

    def arrow(self, a, b, color=INK, width=1.5, head=7, dash=None):
        self.line(a, b, color, width, dash)
        (x1, y1), (x2, y2) = self.map(a), self.map(b)
        ang = math.atan2(y2 - y1, x2 - x1)
        pts = [
            (x2, y2),
            (x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45)),
            (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45)),
        ]
        self.fig.add(_poly(pts, color, color))

    def polygon(self, pts, fill=FACE, stroke=INK, width=1.5, opacity=1.0):
        self.fig.add(_poly([self.map(p) for p in pts], fill, stroke, width, opacity))

    def dot(self, p, r=5, fill=INK, stroke="white"):
        x, y = self.map(p)
        self.fig.add(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1.5"/>'
        )

    def label(self, p, s, size=12, color=INK, dx=0, dy=0, anchor="middle", weight="normal"):
        x, y = self.map(p)
        self.fig.add(_text(x + dx, y + dy, s, size, color, anchor, weight))

    def key(self, p, s, fill=INK, r=10, size=11):
        """A vertex key: a filled circle with its integer inside."""
        x, y = self.map(p)
        self.fig.add(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" '
            'stroke="white" stroke-width="1.5"/>'
        )
        self.fig.add(_text(x, y + size * 0.36, s, size, "white", "middle", "bold"))

    def fkey(self, p, s, color=BLUE, size=12):
        """A face key: a small square tag."""
        x, y = self.map(p)
        r = 10
        self.fig.add(
            f'<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r}" height="{2 * r}" '
            f'rx="3" fill="white" stroke="{color}" stroke-width="1.5"/>'
        )
        self.fig.add(_text(x, y + size * 0.36, s, size, color, "middle", "bold"))


def _text(x, y, s, size, color, anchor="middle", weight="normal"):
    s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
        f'text-anchor="{anchor}" font-weight="{weight}" xml:space="preserve">{s}</text>'
    )


def _poly(pts, fill, stroke, width=1.5, opacity=1.0):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (
        f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{width}" stroke-linejoin="round" fill-opacity="{opacity}"/>'
    )


def xyz(mesh, v):
    return mesh.vertex_coordinates(v)


def all_points(mesh):
    return [xyz(mesh, v) for v in mesh.vertices()]


def lerp(a, b, t):
    return [a[i] + (b[i] - a[i]) * t for i in range(3)]


def hexcolor(rgb):
    return "#%02x%02x%02x" % tuple(int(round(max(0, min(255, c)))) for c in rgb)


def diverging(t):
    """t in [-1, 1]: blue (negative) -> pale grey -> red (positive)."""
    t = max(-1.0, min(1.0, t))
    end = (224, 49, 49) if t > 0 else (28, 126, 214)
    return hexcolor(lerp((236, 238, 241), end, abs(t) ** 0.7))


def sequential(t):
    """t in [0, 1]: pale -> blue -> purple -> orange."""
    stops = [(231, 245, 255), (28, 126, 214), (112, 72, 232), (232, 89, 12)]
    t = max(0.0, min(1.0, t)) * (len(stops) - 1)
    i = min(int(t), len(stops) - 2)
    return hexcolor(lerp(stops[i], stops[i + 1], t - i))


def depth(pts):
    n = len(pts)
    return -sum(p[0] + p[1] for p in pts) / n + sum(p[2] for p in pts) / n


def paint(panel, items):
    for pts, fill, stroke, width in sorted(items, key=lambda it: depth(it[0])):
        panel.polygon(pts, fill, stroke, width)


def facing(normal):
    return -normal[0] - normal[1] + normal[2] > 0


def shaded(base, normal):
    s = 0.72 + 0.28 * max(0.0, -0.35 * normal[0] - 0.75 * normal[1] + 0.56 * normal[2])
    return hexcolor([c * s for c in base])


def solid(panel, mesh, colour=None, stroke=BLUE, width=0.5, cull=True):
    """Iso view of a closed or open mesh, back faces culled, simple shading."""
    items = []
    for f in mesh.faces():
        n = mesh.face_normal(f)
        if cull and not facing(n):
            continue
        fill = colour(f) if colour else shaded((231, 245, 255), n)
        items.append(([xyz(mesh, v) for v in mesh.face_vertices(f)], fill, stroke, width))
    paint(panel, items)


def ball(u=24, v=16, r=1.0):
    return Mesh.from_shape(Sphere(radius=r), u=u, v=v)


def noisy(mesh, amount, seed=0):
    rnd = random.Random(seed)
    out = mesh.copy()
    for v in out.vertices():
        x, y, z = out.vertex_coordinates(v)
        out.vertex_attributes(v, "xyz", [x + rnd.uniform(-amount, amount),
                                         y + rnd.uniform(-amount, amount),
                                         z + rnd.uniform(-amount, amount)])
    return out


def mean_radius(mesh):
    return sum(math.dist(xyz(mesh, v), (0, 0, 0)) for v in mesh.vertices()) / mesh.number_of_vertices()


# ----------------------------------------------------------------------------
# figures
# ----------------------------------------------------------------------------
def fig_smoothing():
    rough = noisy(ball(32, 24), 0.06)
    meshes = [
        (rough, "noisy input"),
        (smoothing.laplacian_smooth(rough, rounds=30), "Laplacian, 30 rounds"),
        (smoothing.taubin_smooth(rough, rounds=30), "Taubin, 30 rounds"),
    ]
    pts = all_points(rough)
    fig = Figure(900, 340)
    for i, (mesh, title) in enumerate(meshes):
        p = Panel(fig, i * 300, 0, 300, 340, pts, view="iso", title=title, pad=34)
        solid(p, mesh)
        fig.add(_text(i * 300 + 150, 312, f"mean radius {mean_radius(mesh):.3f}", 13,
                      RED if i == 1 else INK, weight="bold"))
        fig.add(_text(i * 300 + 150, 330, f"roughness {smoothing.roughness(mesh):.4f}", 12, INK))
    fig.save("alg-smoothing.svg")


def fig_curvature():
    sphere = ball(32, 24)
    saddle = Mesh.from_meshgrid(dx=8, nx=12)
    for v in saddle.vertices():
        x, y, _ = xyz(saddle, v)
        saddle.vertex_attribute(v, "z", 0.07 * ((x - 4) ** 2 - (y - 4) ** 2))
    saddle.quads_to_triangles()
    torus = Mesh.from_shape(Torus(radius_axis=1.6, radius_pipe=0.65), u=40, v=20)
    cases = [(sphere, "sphere: K > 0", True), (saddle, "saddle (triangulated): K < 0", False),
             (torus, "torus: both", True)]
    fig = Figure(900, 350)
    for i, (mesh, title, cull) in enumerate(cases):
        K = curvature.gaussian_curvature(mesh)
        # boundary vertices carry the boundary's turning, not surface
        # curvature -- leave them out of the colours
        K = {v: (0.0 if mesh.is_vertex_on_boundary(v) else k) for v, k in K.items()}
        scale = max(abs(k) for k in K.values())
        p = Panel(fig, i * 300, 0, 300, 350, all_points(mesh), view="iso", title=title, pad=26)

        def colour(f, mesh=mesh, K=K, scale=scale):
            vs = mesh.face_vertices(f)
            return diverging(sum(K[v] for v in vs) / len(vs) / scale)

        solid(p, mesh, colour, "white", 0.3, cull)
        total = curvature.total_curvature(mesh)
        fig.add(_text(i * 300 + 150, 318, f"sum of angle defects = {round(total / math.pi, 4) + 0.0:.4f} π", 13, INK, weight="bold"))
        fig.add(_text(i * 300 + 150, 338, f"2π × euler = 2π × {mesh.euler()}", 12, INK))
    fig.save("alg-curvature.svg")


def fig_geodesics():
    n, size = 24, 12.0
    quads = Mesh.from_meshgrid(dx=size, nx=n)
    tris = Mesh.from_meshgrid(dx=size, nx=n)
    tris.quads_to_triangles()
    centre = [size / 2, size / 2]
    src_q = min(quads.vertices(), key=lambda v: math.dist(xyz(quads, v)[:2], centre))
    src_t = min(tris.vertices(), key=lambda v: math.dist(xyz(tris, v)[:2], centre))
    cases = [
        (quads, geodesics.edge_distances(quads, src_q), "Dijkstra on quad edges", src_q),
        (tris, geodesics.edge_distances(tris, src_t), "Dijkstra on triangle edges", src_t),
        (tris, geodesics.heat_distances(tris, src_t), "heat method (compas_cgal)", src_t),
    ]
    fig = Figure(900, 360)
    for i, (mesh, dist, title, src) in enumerate(cases):
        p = Panel(fig, i * 300, 0, 300, 360, all_points(mesh), title=title, pad=24)
        for f in mesh.faces():
            vs = mesh.face_vertices(f)
            d = sum(dist[v] for v in vs) / len(vs)
            band = int(d / 0.75)
            fill = sequential(min(d / 8.5, 1.0)) if band % 2 == 0 else "#ffffff"
            p.polygon([xyz(mesh, v) for v in vs], fill, fill, 0.6)
        p.key(xyz(mesh, src), "", INK, 5, 1)
        err = sum(abs(dist[v] - math.dist(xyz(mesh, v), xyz(mesh, src))) for v in mesh.vertices()) / mesh.number_of_vertices()
        fig.add(_text(i * 300 + 150, 350, f"mean error vs true distance: {err:.2f} m", 12,
                      RED if err > 0.5 else GREEN, weight="bold"))
    fig.save("alg-geodesics.svg")


def fig_subdivision():
    base = Mesh.from_meshgrid(dx=2, nx=2)
    for v in base.vertices():                      # lift the middle, for interest
        x, y, _ = xyz(base, v)
        if (x, y) == (1.0, 1.0):
            base.vertex_attribute(v, "z", 0.0)
    out = subdivision.catmull_clark(base)
    fig = Figure(900, 385)

    p = Panel(fig, 0, 0, 340, 360, all_points(base), title="one round on a 2×2 grid", pad=40)
    for f in out.faces():
        p.polygon([xyz(out, v) for v in out.face_vertices(f)], "none", GREY, 1)
    for f in base.faces():
        p.polygon([xyz(base, v) for v in base.face_vertices(f)], "none", INK, 2.2)
    V, E, F = base.number_of_vertices(), base.number_of_edges(), base.number_of_faces()
    keys = list(out.vertices())
    for k in keys[:V]:
        p.dot(xyz(out, k), 6, GREEN)
    for k in keys[V:V + E]:
        p.dot(xyz(out, k), 6, ORANGE)
    for k in keys[V + E:]:
        p.dot(xyz(out, k), 6, BLUE)
    fig.add(_text(70, 356, "● face points", 12, BLUE, "start"))
    fig.add(_text(160, 356, "● edge points", 12, ORANGE, "start"))
    fig.add(_text(250, 356, "● moved vertices", 12, GREEN, "start"))
    fig.add(_text(170, 376, f"V' = V + E + F = {V} + {E} + {F} = {out.number_of_vertices()}", 12, INK, weight="bold"))
    for i, k in enumerate((1, 2)):
        mesh = Mesh.from_polyhedron(6)
        for _ in range(k):
            mesh = subdivision.catmull_clark(mesh)
        p = Panel(fig, 340 + i * 280, 0, 280, 360, all_points(Mesh.from_polyhedron(6)), view="iso",
                  title=f"cube, {k} round{'s' if k > 1 else ''} (our code)", pad=40)
        solid(p, mesh)
        fig.add(_text(340 + i * 280 + 140, 356, f"V={mesh.number_of_vertices()} F={mesh.number_of_faces()} euler={mesh.euler()}", 12, INK))
    fig.save("alg-subdivision.svg")


def dome(n=10, size=10.0, radius=8.0):
    mesh = Mesh.from_meshgrid(dx=size, nx=n)
    for v in mesh.vertices():
        x, y, _ = xyz(mesh, v)
        r2 = (x - size / 2) ** 2 + (y - size / 2) ** 2
        mesh.vertex_attribute(v, "z", math.sqrt(radius ** 2 - r2) - math.sqrt(radius ** 2 - 2 * (size / 2) ** 2))
    return mesh


def fig_planarity():
    before = dome()
    fixed = [v for v in before.vertices() if before.vertex_degree(v) == 2]
    after = planarity.planarize(before, fixed=fixed, rounds=200)
    worst = max(planarity.flatness(before, f) for f in before.faces())
    fig = Figure(900, 370)
    for i, (mesh, title) in enumerate([(before, "a spherical dome on a square grid"), (after, "after planarize(), 200 rounds")]):
        p = Panel(fig, i * 450, 0, 450, 370, all_points(before), view="iso", title=title, pad=30)

        def colour(f, mesh=mesh):
            fl = planarity.flatness(mesh, f)
            return GREEN if fl < 0.005 else sequential(0.25 + 0.75 * min(fl / worst, 1))

        solid(p, mesh, colour, "white", 0.8, cull=False)
        fl = max(planarity.flatness(mesh, f) for f in mesh.faces())
        fig.add(_text(i * 450 + 225, 336, f"worst panel flatness {fl:.2%}", 14, GREEN if fl < 0.005 else RED, weight="bold"))
    drift = max(math.dist(xyz(before, v), xyz(after, v)) for v in before.vertices())
    fig.add(_text(225, 358, "orange: twisted panels -- glass would have to be bent", 12, INK))
    fig.add(_text(675, 358, f"green: flatness < 0.5%; the price: vertices moved up to {drift * 100:.0f} cm", 12, INK))
    fig.save("alg-planarity.svg")


def terrain():
    mesh = Mesh.from_meshgrid(dx=12, nx=36, dy=8, ny=24)
    for v in mesh.vertices():
        x, y, _ = xyz(mesh, v)
        z = (1.6 * math.exp(-((x - 3.5) ** 2 + (y - 4.5) ** 2) / 3)
             + 1.1 * math.exp(-((x - 8.5) ** 2 + (y - 3) ** 2) / 2.5)
             + 0.08 * x)
        mesh.vertex_attribute(v, "z", z)
    mesh.quads_to_triangles()
    return mesh


def fig_contours():
    mesh = terrain()
    heights = [0.15 + 0.2 * i for i in range(10)]
    zmax = max(mesh.vertices_attribute("z"))
    fig = Figure(900, 360)
    p = Panel(fig, 0, 0, 450, 360, all_points(mesh), view="iso", title="terrain + contours(mesh, h)", pad=24)
    solid(p, mesh, lambda f: "#f1f3f5", "#dee2e6", 0.3, cull=False)
    for h in heights:
        for line in contouring.contours(mesh, h):
            for a, b in zip(line, line[1:]):
                p.line(a, b, sequential(0.3 + 0.7 * h / zmax), 1.8)
    p = Panel(fig, 450, 0, 450, 360, all_points(mesh), title="plan: one closed loop per hill, open on the slope", pad=24)
    count_closed = count_open = 0
    for h in heights:
        for line in contouring.contours(mesh, h):
            closed = math.dist(line[0], line[-1]) < 1e-9
            count_closed += closed
            count_open += not closed
            for a, b in zip(line, line[1:]):
                p.line(a, b, sequential(0.3 + 0.7 * h / zmax), 2)
    fig.add(_text(675, 350, f"{count_closed} closed + {count_open} open polylines, chained by edge key, no tolerance", 12, INK))
    fig.add(_text(225, 350, "every 0.2 m: a site model, print layers, waffle ribs", 12, INK))
    fig.save("alg-contours.svg")


def fig_voronoi():
    rnd = random.Random(11)
    pts = [[rnd.uniform(0, 10), rnd.uniform(0, 6), 0] for _ in range(45)]
    mesh = voronoi.delaunay(pts)
    cells = voronoi.voronoi_cells(mesh)
    fig = Figure(900, 330)
    titles = ["Delaunay triangulation", "the empty-circle property", "Voronoi: the dual, at circumcentres"]
    for i, title in enumerate(titles):
        p = Panel(fig, i * 300, 0, 300, 330, pts, title=title, pad=26)
        if i < 2:
            for f in mesh.faces():
                p.polygon([xyz(mesh, v) for v in mesh.face_vertices(f)], FACE if i == 0 else "white", BLUE, 1)
        if i == 1:
            f = max((f for f in mesh.faces() if not mesh.is_face_on_boundary(f)),
                    key=lambda f: mesh.face_area(f))
            tri = [xyz(mesh, v) for v in mesh.face_vertices(f)]
            c = voronoi.circumcentre(*tri)
            r = math.dist(c, tri[0])
            p.polygon(tri, "#ffe8cc", ORANGE, 2)
            ring = [[c[0] + r * math.cos(t / 48 * 2 * math.pi), c[1] + r * math.sin(t / 48 * 2 * math.pi), 0] for t in range(48)]
            p.polygon(ring, "none", ORANGE, 2)
            p.dot(c, 4, ORANGE)
        if i == 2:
            for k, (v, cell) in enumerate(cells.items()):
                # cells next to the hull reach far out (thin hull triangles
                # have distant circumcentres) -- draw only the ones that fit
                if all(0 <= c[0] <= 10 and 0 <= c[1] <= 6 for c in cell):
                    p.polygon(cell, sequential(0.08 + 0.3 * ((k * 7) % 10) / 10), PURPLE, 1.5)
        for q in pts:
            p.dot(q, 3, INK)
    fig.add(_text(450, 322, f"{len(pts)} points, {mesh.number_of_faces()} triangles, "
                  f"{len(cells)} bounded cells (one per interior point; those reaching past the frame not drawn)", 12, INK))
    fig.save("alg-voronoi.svg")


def fig_skeleton():
    from compas_cgal.straight_skeleton_2 import interior_straight_skeleton

    footprint = [[0, 0, 0], [12, 0, 0], [12, 5, 0], [5, 5, 0], [5, 11, 0], [0, 11, 0]]
    graph = interior_straight_skeleton(footprint)
    edges = [(a, b) for a, b in zip(footprint, footprint[1:] + footprint[:1])]

    def to_edge(p, a, b):
        ab = [b[i] - a[i] for i in range(2)]
        t = max(0, min(1, ((p[0] - a[0]) * ab[0] + (p[1] - a[1]) * ab[1]) / (ab[0] ** 2 + ab[1] ** 2)))
        return math.dist(p[:2], [a[0] + t * ab[0], a[1] + t * ab[1]])

    slope = math.tan(math.radians(30))
    roof = {n: [*graph.node_coordinates(n)[:2], slope * min(to_edge(graph.node_coordinates(n), a, b) for a, b in edges)]
            for n in graph.nodes()}
    pts = list(roof.values())
    fig = Figure(900, 360)
    p = Panel(fig, 0, 0, 400, 360, pts, title="straight skeleton of an L-shaped plan", pad=34)
    p.polygon(footprint, LIGHT, INK, 2)
    for u, v in graph.edges():
        if not graph.edge_attribute((u, v), "boundary"):
            p.line(graph.node_coordinates(u), graph.node_coordinates(v), ORANGE, 2.5)
    p = Panel(fig, 400, 0, 500, 360, pts, view="iso", title="lift each node by its distance to the eaves: a hip roof", pad=34)
    for u, v in sorted(graph.edges(), key=lambda e: depth([roof[e[0]], roof[e[1]]])):
        boundary = graph.edge_attribute((u, v), "boundary")
        p.line(roof[u], roof[v], INK if boundary else ORANGE, 2 if boundary else 2.5)
    fig.add(_text(200, 350, "compas_cgal: interior_straight_skeleton(footprint)", 12, INK))
    fig.add(_text(650, 350, "30° pitch everywhere -- every roof plane rises at the same rate", 12, INK))
    fig.save("alg-skeleton.svg")


def fig_hull():
    rnd = random.Random(21)
    pts = [[rnd.gauss(5, 1.6), rnd.gauss(3, 1.0), 0] for _ in range(70)]
    hull = convex_hull.convex_hull(pts)
    fig = Figure(900, 330)
    p = Panel(fig, 0, 0, 450, 330, pts, title="convex_hull(points): the rubber band", pad=30)
    p.polygon(hull, FACE, BLUE, 2.5)
    for q in pts:
        p.dot(q, 3, GREY)
    for i, q in enumerate(hull):
        p.key(q, i, BLUE, 9, 10)
    # the monotone chain, explained on 6 points
    demo = [[0, 0, 0], [1, 1.6, 0], [2, 0.6, 0], [3, 2.2, 0], [4, 1.0, 0], [5, 0.2, 0]]
    p = Panel(fig, 450, 0, 450, 330, demo + [[0, -0.8, 0], [5, 2.6, 0]], title="the walk drops every right turn", pad=34)
    hull_demo = convex_hull.convex_hull(demo)
    for a, b in zip(demo, demo[1:]):
        p.line(a, b, GREY, 1.5, dash="4,4")
    for a, b in zip(hull_demo, hull_demo[1:] + hull_demo[:1]):
        p.line(a, b, BLUE, 2.5)
    corners = {tuple(q[:2]) for q in hull_demo}
    dropped = [i for i, q in enumerate(demo) if tuple(q[:2]) not in corners]
    for i, q in enumerate(demo):
        p.key(q, i, BLUE if tuple(q[:2]) in corners else GREY, 9, 10)
    p.label([2.5, -0.55, 0], f"{' and '.join(map(str, dropped))} turn right relative to their neighbours: inside, dropped", 12, INK)
    fig.add(_text(225, 322, f"{len(pts)} points -> {len(hull)} corners, counter-clockwise", 12, INK))
    fig.save("alg-hull.svg")


def fig_nearest():
    import time
    rnd = random.Random(4)
    sizes = [250, 500, 1000, 2000, 4000]
    brute, hashed = [], []
    for n in sizes:
        pts = [[rnd.uniform(0, 100), rnd.uniform(0, 60), 0] for _ in range(n)]
        r = 2.0
        t = time.perf_counter(); nearest.all_pairs_hashed(pts, r); hashed.append(time.perf_counter() - t)
        if n <= 2000:
            t = time.perf_counter(); nearest.all_pairs_brute(pts, r); brute.append(time.perf_counter() - t)
    brute.append(brute[-1] * 4)          # O(n^2): doubling n quadruples the time
    fig = Figure(900, 360)
    # left: the grid idea
    pts = [[rnd.uniform(0, 10), rnd.uniform(0, 6), 0] for _ in range(160)]
    grid = nearest.SpatialHash(pts, 1.0)
    q = min(range(len(pts)), key=lambda i: math.dist(pts[i][:2], (5.3, 3.4)))
    p = Panel(fig, 0, 0, 430, 360, [[0, 0, 0], [10, 6, 0]], title="a spatial hash: look in 9 cells, not everywhere", pad=26)
    cx, cy = grid._key(pts[q])
    for i in range(0, 11):
        p.line([i, 0, 0], [i, 6, 0], LIGHT if True else GREY, 1)
    for j in range(0, 7):
        p.line([0, j, 0], [10, j, 0], LIGHT, 1)
    p.polygon([[cx - 1, cy - 1, 0], [cx + 2, cy - 1, 0], [cx + 2, cy + 2, 0], [cx - 1, cy + 2, 0]], "#fff4e6", ORANGE, 2)
    near = set(grid.within(q))
    for i, pt in enumerate(pts):
        p.dot(pt, 3.5 if i in near else 2.5, ORANGE if i in near else GREY)
    p.dot(pts[q], 6, BLUE)
    ring = [[pts[q][0] + math.cos(t / 40 * 2 * math.pi), pts[q][1] + math.sin(t / 40 * 2 * math.pi), 0] for t in range(40)]
    p.polygon(ring, "none", BLUE, 1.5)
    # right: timing
    x0, y0, w, h = 500, 60, 360, 240
    tmax = max(brute)
    fig.add(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="white" stroke="{GREY}"/>')
    fig.add(_text(x0 + w / 2, 38, "all neighbours within r: seconds", 15, INK, weight="bold"))
    def xy(i, t):
        return x0 + 20 + i * (w - 40) / (len(sizes) - 1), y0 + h - 10 - (h - 20) * t / tmax
    for series, colour, label in ((brute, RED, "brute force, O(n²)"), (hashed, GREEN, "spatial hash, ~O(n)")):
        pts2 = [xy(i, t) for i, t in enumerate(series)]
        fig.add('<polyline points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts2) + f'" fill="none" stroke="{colour}" stroke-width="3"/>')
        for a, b in pts2:
            fig.add(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="4" fill="{colour}"/>')
        fig.add(_text(pts2[-1][0] - 6, pts2[-1][1] - 10, label, 12, colour, "end", "bold"))
    for i, n in enumerate(sizes):
        a, _ = xy(i, 0)
        fig.add(_text(a, y0 + h + 18, f"{n}", 11, INK))
    fig.add(_text(x0 + w / 2, y0 + h + 36, "points (the 4000-point brute-force value is extrapolated ×4)", 11, INK))
    fig.add(_text(x0 + w / 2, y0 + h + 52, f"at 2000 points: {brute[3]:.2f} s vs {hashed[3]:.3f} s, same answers", 12, INK, weight="bold"))
    fig.save("alg-nearest.svg")


def fig_lloyd():
    rnd = random.Random(12)
    sites = [(rnd.uniform(0, 10), rnd.uniform(0, 6)) for _ in range(28)]
    smp = lloyd.samples(10, 6, 70)
    after, history = lloyd.lloyd(sites, smp, rounds=25)
    fig = Figure(900, 360)
    palette = [hexcolor(c) for c in [(231, 245, 255), (255, 244, 230), (235, 251, 238), (243, 240, 255), (255, 240, 246), (248, 249, 250)]]
    for i, (sts, title) in enumerate([(sites, "random sites"), (after, "after 25 rounds of Lloyd")]):
        p = Panel(fig, i * 450, 0, 450, 330, [[0, 0, 0], [10, 6, 0]], title=title, pad=24)
        owner = lloyd.assign(sts, smp)
        d = 10 / 70
        for s, k in zip(smp, owner):
            p.polygon([[s[0] - d / 2, s[1] - d / 2, 0], [s[0] + d / 2, s[1] - d / 2, 0],
                       [s[0] + d / 2, s[1] + d / 2, 0], [s[0] - d / 2, s[1] + d / 2, 0]],
                      palette[k % len(palette)], "none", 0)
        for q in sts:
            p.dot([q[0], q[1], 0], 4.5, INK)
        gaps = lloyd.nearest_spacing(sts)
        fig.add(_text(i * 450 + 225, 338, f"closest pair {min(gaps):.2f} m; spacing {min(gaps):.2f}–{max(gaps):.2f} m", 12, INK, weight="bold"))
    fig.add(_text(450, 356, f"energy (sum of squared sample distances) {history[0]:.0f} → {history[-1]:.0f}, never increasing", 12, INK))
    fig.save("alg-lloyd.svg")


if __name__ == "__main__":
    fig_smoothing()
    fig_curvature()
    fig_geodesics()
    fig_subdivision()
    fig_planarity()
    fig_contours()
    fig_voronoi()
    fig_skeleton()
    fig_hull()
    fig_nearest()
    fig_lloyd()
