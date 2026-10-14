"""
Draw every figure in the Week 05 README and notebooks -- from real COMPAS meshes.

    uv run Lecture/Lecture_05/figures/make_figures.py

Nothing here is hand-drawn. Each picture is built by calling the same Mesh
methods the README teaches, then writing the result out as a plain SVG file.
So the vertex keys, face keys, neighbours and counts you see in a figure are
exactly what you get when you run the code yourself.

You do not need to read this file to follow the lecture. It is here for two
reasons: so the figures can be regenerated if COMPAS changes, and as a worked
example of using a mesh as *data* -- this script never opens a viewer.
"""

import math
import sys
from pathlib import Path

from compas.datastructures import Mesh
from compas.geometry import Sphere

HERE = Path(__file__).parent

# the application figures are drawn from the scripts students run
sys.path.insert(0, str(HERE.parent / "mesh_applications"))
import cloth_simulation  # noqa: E402
import form_finding  # noqa: E402
import scan_to_mesh  # noqa: E402
import structural_analysis  # noqa: E402

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


# ----------------------------------------------------------------------------
# helpers that read a mesh
# ----------------------------------------------------------------------------
def xyz(mesh, v):
    return mesh.vertex_coordinates(v)


def all_points(mesh):
    return [xyz(mesh, v) for v in mesh.vertices()]


def draw_faces(panel, mesh, fill=FACE, stroke=INK, faces=None, width=1.5):
    for f in faces if faces is not None else mesh.faces():
        panel.polygon([xyz(mesh, v) for v in mesh.face_vertices(f)], fill, stroke, width)


def draw_edges(panel, mesh, color=INK, width=1.5, edges=None):
    for u, v in edges if edges is not None else mesh.edges():
        panel.line(xyz(mesh, u), xyz(mesh, v), color, width)


def lerp(a, b, t):
    return [a[i] + (b[i] - a[i]) * t for i in range(3)]


def hexcolor(rgb):
    return "#%02x%02x%02x" % tuple(int(round(c)) for c in rgb)


def ramp(t):
    """Blue -> yellow -> red, t in [0, 1]."""
    stops = [(43, 108, 176), (255, 212, 59), (224, 49, 49)]
    if t <= 0.5:
        return hexcolor(lerp(stops[0], stops[1], t * 2))
    return hexcolor(lerp(stops[1], stops[2], (t - 0.5) * 2))


def grid(nx, ny, spacing=1.0):
    """The same grid the checkpoint asks for: x-fastest keys, CCW quads."""
    mesh = Mesh()
    key = {}
    for j in range(ny + 1):
        for i in range(nx + 1):
            key[i, j] = mesh.add_vertex(x=i * spacing, y=j * spacing, z=0)
    for j in range(ny):
        for i in range(nx):
            mesh.add_face([key[i, j], key[i + 1, j], key[i + 1, j + 1], key[i, j + 1]])
    return mesh


# ----------------------------------------------------------------------------
# the figures
# ----------------------------------------------------------------------------
def fig_soup_vs_mesh():
    fig = Figure(860, 330)

    # left: a "triangle soup" -- two triangles that merely LOOK connected
    soup = [
        [[0, 0, 0], [2, 0, 0], [2, 2, 0]],
        [[0, 0, 0], [2, 2, 0], [0, 2, 0]],
    ]
    p = Panel(fig, 0, 0, 430, 330, [q for t in soup for q in t] + [[1, -0.8, 0]], title="A list of triangles")
    shift = [[0.12, -0.08, 0], [-0.12, 0.08, 0]]
    for t, (sx, sy, _) in zip(soup, shift):
        pts = [[q[0] + sx, q[1] + sy, 0] for q in t]
        p.polygon(pts, "#fff4e6", ORANGE)
        for q in pts:
            p.dot(q, 4, ORANGE)
    p.label([1, -0.45, 0], "6 points -- the shared corners stored twice", 12, ORANGE)
    p.label([1, -0.75, 0], "who touches whom? compare floats", 12, INK)

    # right: an indexed mesh -- faces refer to SHARED vertex keys
    mesh = Mesh.from_vertices_and_faces(
        [[0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0]], [[0, 1, 2], [0, 2, 3]]
    )
    p = Panel(fig, 430, 0, 430, 330, all_points(mesh) + [[1, -0.8, 0]], title="A mesh")
    draw_faces(p, mesh)
    for f in mesh.faces():
        p.fkey(mesh.face_centroid(f), f)
    for v in mesh.vertices():
        p.key(xyz(mesh, v), v)
    p.label([1, -0.45, 0], "4 vertices -- faces [0, 1, 2] and [0, 2, 3]", 12, BLUE)
    p.label([1, -0.75, 0], "edge (0, 2) is shared -- by key", 12, INK)
    fig.save("mesh-soup-vs-mesh.svg")


def fig_anatomy():
    mesh = grid(3, 2)
    fig = Figure(860, 380)
    p = Panel(fig, 0, 0, 860, 380, all_points(mesh), pad=50,
              title="grid(3, 2): 12 vertices, 17 edges, 6 faces")
    draw_faces(p, mesh)
    # edge keys as (u, v) on a few edges, to show what an edge IS
    for u, v in [(0, 1), (5, 6), (6, 10)]:
        mid = mesh.edge_midpoint((u, v))
        p.line(xyz(mesh, u), xyz(mesh, v), ORANGE, 4)
        off = (0, -12) if abs(xyz(mesh, u)[1] - xyz(mesh, v)[1]) < 1e-9 else (30, 4)
        p.label(mid, f"({u}, {v})", 12, ORANGE, *off, weight="bold")
    for f in mesh.faces():
        p.fkey(mesh.face_centroid(f), f)
    for v in mesh.vertices():
        p.key(xyz(mesh, v), v)
    fig.add(_text(30, 368, "● vertex key", 12, INK, "start"))
    fig.add(_text(140, 368, "▢ face key", 12, BLUE, "start"))
    fig.add(_text(240, 368, "— edge = a pair of vertex keys", 12, ORANGE, "start"))
    fig.save("mesh-anatomy.svg")


def fig_winding():
    fig = Figure(860, 330)
    pts = [[0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0]]
    for i, (order, title, color, up) in enumerate([
        ([0, 1, 2, 3], "add_face([0, 1, 2, 3])  counter-clockwise", BLUE, True),
        ([0, 3, 2, 1], "add_face([0, 3, 2, 1])  clockwise", RED, False),
    ]):
        mesh = Mesh.from_vertices_and_faces(pts, [order])
        p = Panel(fig, i * 430, 0, 430, 330, pts, title=title, pad=55)
        draw_faces(p, mesh, fill=FACE if up else "#fff5f5", stroke=GREY)
        cyc = mesh.face_vertices(0)
        c = mesh.face_centroid(0)
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            A = lerp(xyz(mesh, a), c, 0.22)
            B = lerp(xyz(mesh, b), c, 0.22)
            p.arrow(lerp(A, B, 0.1), lerp(A, B, 0.9), color, 2.2)
        for v in mesh.vertices():
            p.key(xyz(mesh, v), v)
        n = mesh.face_normal(0)
        x, y = p.map(c)
        fig.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="white" stroke="{color}" stroke-width="2"/>')
        if up:
            fig.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}"/>')
        else:
            fig.add(f'<path d="M{x - 7:.1f},{y - 7:.1f} L{x + 7:.1f},{y + 7:.1f} M{x + 7:.1f},{y - 7:.1f} L{x - 7:.1f},{y + 7:.1f}" stroke="{color}" stroke-width="2"/>')
        p.label([1, -0.45, 0], f"face_normal(0) = [0, 0, {n[2]:+.0f}]", 13, color, weight="bold")
    fig.save("mesh-winding.svg")


def fig_halfedges():
    mesh = grid(2, 1)
    fig = Figure(860, 400)
    p = Panel(fig, 0, 0, 860, 400, all_points(mesh), pad=70,
              title="Every edge is two halfedges, one per side")
    draw_faces(p, mesh, stroke=GREY)
    for u in mesh.halfedge:
        for v in mesh.halfedge[u]:
            f = mesh.halfedge_face((u, v))
            a, b = xyz(mesh, u), xyz(mesh, v)
            d = [b[0] - a[0], b[1] - a[1], 0]
            L = math.hypot(d[0], d[1])
            nrm = [-d[1] / L, d[0] / L, 0]   # left of (u -> v)
            off = 0.09
            A = [a[i] + nrm[i] * off for i in range(3)]
            B = [b[i] + nrm[i] * off for i in range(3)]
            if f is None:
                p.arrow(lerp(A, B, 0.2), lerp(A, B, 0.8), GREY, 1.6, dash="5,4")
            else:
                p.arrow(lerp(A, B, 0.2), lerp(A, B, 0.8), [BLUE, GREEN][f], 2)
    for f in mesh.faces():
        p.fkey(mesh.face_centroid(f), f, [BLUE, GREEN][f])
    for v in mesh.vertices():
        p.key(xyz(mesh, v), v)
    p.label(mesh.face_centroid(0), "halfedge (1, 4) → face 0", 12, BLUE, 0, 34, weight="bold")
    p.label(mesh.face_centroid(1), "halfedge (4, 1) → face 1", 12, GREEN, 0, 34, weight="bold")
    fig.add(_text(430, 388, "dashed: boundary halfedges -- mesh.halfedge_face((u, v)) is None", 12, INK))
    fig.save("mesh-halfedges.svg")


def fig_neighbours():
    mesh = grid(4, 4)
    fig = Figure(900, 340)
    v = 12            # the middle vertex
    f = 5             # an interior face
    panels = [
        ("vertex_neighbors(12)", "v"),
        ("vertex_faces(12)", "vf"),
        ("face_neighbors(5)", "f"),
    ]
    for i, (title, kind) in enumerate(panels):
        p = Panel(fig, i * 300, 0, 300, 340, all_points(mesh), title=title, pad=28)
        hi = []
        if kind == "vf":
            hi = mesh.vertex_faces(v)
        if kind == "f":
            hi = mesh.face_neighbors(f)
        draw_faces(p, mesh, fill="white", stroke=GREY, width=1)
        draw_faces(p, mesh, fill="#ffe8cc", stroke=GREY, faces=hi, width=1)
        if kind == "f":
            draw_faces(p, mesh, fill=BLUE, stroke=GREY, faces=[f], width=1)
            for g in hi:
                p.fkey(mesh.face_centroid(g), g, ORANGE, 11)
            p.fkey(mesh.face_centroid(f), f, BLUE, 11)
        else:
            if kind == "v":
                for n in mesh.vertex_neighbors(v):
                    p.line(xyz(mesh, v), xyz(mesh, n), ORANGE, 3)
                for n in mesh.vertex_neighbors(v):
                    p.key(xyz(mesh, n), n, ORANGE, 9, 10)
            else:
                for g in hi:
                    p.fkey(mesh.face_centroid(g), g, ORANGE, 11)
            p.key(xyz(mesh, v), v, BLUE, 9, 10)
    fig.save("mesh-neighbours.svg")


def fig_boundary():
    mesh = grid(4, 3)
    fig = Figure(860, 380)
    p = Panel(fig, 0, 0, 860, 380, all_points(mesh), pad=46,
              title="Boundary: vertices_on_boundary() and edges_on_boundary()")
    draw_faces(p, mesh, stroke=GREY, width=1)
    draw_edges(p, mesh, ORANGE, 4, edges=mesh.edges_on_boundary())
    for k in mesh.vertices():
        if mesh.is_vertex_on_boundary(k):
            p.key(xyz(mesh, k), k, ORANGE, 10)
        else:
            p.key(xyz(mesh, k), k, GREY, 10)
    cycle = mesh.vertices_on_boundary()
    fig.add(_text(430, 366, f"vertices_on_boundary() has {len(cycle)} items "
                  f"for {len(set(cycle))} distinct vertices -- it is a closed cycle",
                  12, ORANGE))
    fig.save("mesh-boundary.svg")


def fig_loops_strips():
    mesh = grid(5, 4)
    fig = Figure(860, 360)
    start = (8, 9)
    for i, (title, kind) in enumerate([
        (f"edge_loop({start})", "loop"),
        (f"edge_strip({start})", "strip"),
    ]):
        p = Panel(fig, i * 430, 0, 430, 360, all_points(mesh), title=title, pad=32)
        if kind == "loop":
            draw_faces(p, mesh, fill="white", stroke=GREY, width=1)
            draw_edges(p, mesh, ORANGE, 4, edges=list(mesh.edge_loop(start)))
        else:
            strip = list(mesh.edge_strip(start))
            faces = {mesh.halfedge_face(e) for e in strip} | {
                mesh.halfedge_face((e[1], e[0])) for e in strip}
            faces.discard(None)
            draw_faces(p, mesh, fill="white", stroke=GREY, width=1)
            draw_faces(p, mesh, fill="#ffe8cc", stroke=GREY, faces=faces, width=1)
            draw_edges(p, mesh, ORANGE, 4, edges=strip)
        p.line(xyz(mesh, start[0]), xyz(mesh, start[1]), BLUE, 5)
        p.key(xyz(mesh, start[0]), start[0], BLUE, 9, 10)
        p.key(xyz(mesh, start[1]), start[1], BLUE, 9, 10)
    fig.add(_text(215, 350, "edges end to end, straight through each vertex", 12, INK))
    fig.add(_text(645, 350, "edges side by side, across a row of quads", 12, INK))
    fig.save("mesh-loops-strips.svg")


def wave(mesh, amplitude=0.9, wavelength=4.0):
    """The checkpoint-4 deformation (a sine along x), plus a gentle tilt in y."""
    for k in mesh.vertices():
        x, y, z = xyz(mesh, k)
        z = amplitude * math.sin(2 * math.pi * x / wavelength) + 0.15 * y
        mesh.vertex_attribute(k, "z", z)
    return mesh


def fig_attributes():
    mesh = wave(grid(8, 8, 0.5))
    heights = mesh.vertices_attribute("z")
    lo, hi = min(heights), max(heights)
    for k in mesh.vertices():
        t = (mesh.vertex_attribute(k, "z") - lo) / (hi - lo)
        mesh.vertex_attribute(k, "color", ramp(t))
    fig = Figure(860, 400)
    p = Panel(fig, 0, 0, 560, 400, all_points(mesh), view="iso", pad=30,
              title='vertex_attribute(key, "color", ...) by height')
    # back-to-front so near faces cover far ones
    order = sorted(mesh.faces(), key=lambda f: -sum(mesh.face_centroid(f)[:2]))
    for f in order:
        vs = mesh.face_vertices(f)
        z = sum(mesh.vertex_attribute(v, "z") for v in vs) / len(vs)
        p.polygon([xyz(mesh, v) for v in vs], ramp((z - lo) / (hi - lo)), "white", 0.8)
    # the dictionary on one vertex
    k = 38
    p.key(xyz(mesh, k), k, INK, 10, 10)
    attrs = mesh.vertex_attributes(k)
    lines = [f"mesh.vertex_attributes({k})", "{"] + [
        f'  "{name}": {attrs[name]:.2f},' for name in ("x", "y", "z")
    ] + [f'  "color": "{attrs["color"]}",', "}"]
    for i, s in enumerate(lines):
        fig.add(_text(590, 120 + i * 22, s, 14, INK if i else BLUE, "start",
                      "bold" if i == 0 else "normal"))
    fig.add(_text(590, 120 + len(lines) * 22 + 16, "x, y, z are attributes too --", 12, INK, "start"))
    fig.add(_text(590, 120 + len(lines) * 22 + 34, "that is how a vertex moves", 12, INK, "start"))
    fig.save("mesh-attributes.svg")


def fig_euler():
    fig = Figure(900, 350)

    good = grid(3, 2)

    holed = grid(3, 3)
    holed.delete_face(4)   # the middle face

    split = Mesh()       # two faces that LOOK joined but do not share vertices
    a = [split.add_vertex(x=x, y=y, z=0) for x, y in [(0, 0), (1, 0), (1, 1), (0, 1)]]
    b = [split.add_vertex(x=x, y=y, z=0) for x, y in [(1, 0), (2, 0), (2, 1), (1, 1)]]
    split.add_face(a)
    split.add_face(b)

    cases = [
        (good, "a flat grid", GREEN),
        (holed, "a grid with a hole", BLUE),
        (split, "duplicated vertices (bug)", RED),
    ]
    for i, (mesh, title, color) in enumerate(cases):
        p = Panel(fig, i * 300, 0, 300, 350, all_points(mesh), title=title, pad=50)
        draw_faces(p, mesh, fill="white" if color == RED else FACE, stroke=color, width=2)
        for k in mesh.vertices():
            p.dot(xyz(mesh, k), 4, color)
        if mesh is split:
            p.label([1, 1, 0], "x2", 12, RED, 14, -8, "start", "bold")
            p.label([1, 0, 0], "x2", 12, RED, 14, 16, "start", "bold")
        V, E, F = mesh.number_of_vertices(), mesh.number_of_edges(), mesh.number_of_faces()
        fig.add(_text(i * 300 + 150, 318, f"V - E + F = {V} - {E} + {F} = {mesh.euler()}",
                      14, color, weight="bold"))
    fig.save("mesh-euler.svg")


def fig_deform():
    flat = grid(8, 4, 0.5)
    bent = wave(grid(8, 4, 0.5), amplitude=0.8)
    pts = all_points(flat) + all_points(bent)
    fig = Figure(860, 340)
    for i, (mesh, title) in enumerate([(flat, "before"), (bent, "after: only z changed")]):
        p = Panel(fig, i * 430, 0, 430, 340, pts, view="iso", title=title, pad=30)
        order = sorted(mesh.faces(), key=lambda f: -sum(mesh.face_centroid(f)[:2]))
        for f in order:
            p.polygon([xyz(mesh, v) for v in mesh.face_vertices(f)], FACE, BLUE, 1)
        p.key(xyz(mesh, 0), 0, INK, 8, 9)
        p.key(xyz(mesh, 8), 8, INK, 8, 9)
    fig.add(_text(430, 328, f"same {flat.number_of_vertices()} vertex keys, "
                  f"same {flat.number_of_faces()} faces, same edges -- no face was rebuilt",
                  13, INK))
    fig.save("mesh-deform.svg")


def fig_subdivide():
    base = Mesh.from_polyhedron(6)
    meshes = [base, base.subdivided("catmullclark", k=1), base.subdivided("catmullclark", k=2)]
    pts = all_points(base)
    fig = Figure(900, 320)
    for i, mesh in enumerate(meshes):
        title = "Mesh.from_polyhedron(6)" if i == 0 else f'subdivided("catmullclark", k={i})'
        p = Panel(fig, i * 300, 0, 300, 320, pts, view="iso", title=title, pad=40)
        # painter's order, viewed from the front-left
        order = sorted(mesh.faces(), key=lambda f: (lambda c: -(c[0] + c[1]) + c[2])(mesh.face_centroid(f)))
        light = [-0.35, -0.75, 0.56]
        for f in order:
            n = mesh.face_normal(f)
            if -n[0] - n[1] + n[2] <= 0:      # facing away from us: skip it
                continue
            shade = 0.72 + 0.28 * max(0.0, sum(a * b for a, b in zip(n, light)))
            fill = hexcolor([231 * shade, 245 * shade, 255 * shade])
            p.polygon([xyz(mesh, v) for v in mesh.face_vertices(f)], fill, BLUE, 0.8)
        fig.add(_text(i * 300 + 150, 308, f"V={mesh.number_of_vertices()}  F={mesh.number_of_faces()}  "
                      f"euler={mesh.euler()}", 12, INK))
    fig.save("mesh-subdivide.svg")


def fig_dual():
    mesh = grid(4, 3)
    dual = mesh.dual(include_boundary=False)
    fig = Figure(860, 360)
    p = Panel(fig, 0, 0, 860, 360, all_points(mesh), pad=40,
              title="mesh.dual(): a vertex per face, a face per interior vertex")
    draw_faces(p, mesh, fill="white", stroke=GREY, width=1)
    for f in dual.faces():
        p.polygon([dual.vertex_coordinates(v) for v in dual.face_vertices(f)], "#ffe8cc", ORANGE, 2.5, 0.6)
    for v in dual.vertices():
        p.dot(dual.vertex_coordinates(v), 5, ORANGE)
    fig.add(_text(430, 348, f"original: {mesh.number_of_faces()} faces, "
                  f"{sum(not mesh.is_vertex_on_boundary(k) for k in mesh.vertices())} interior vertices"
                  f"  →  dual: {dual.number_of_vertices()} vertices, {dual.number_of_faces()} faces",
                  12, INK))
    fig.save("mesh-dual.svg")


# ----------------------------------------------------------------------------
# applications (section 12) -- drawn from ../mesh_applications/*.py
# ----------------------------------------------------------------------------
def depth(pts):
    """Painter's depth for the iso view: far = high x + y, low z."""
    n = len(pts)
    return -sum(p[0] + p[1] for p in pts) / n + sum(p[2] for p in pts) / n


def paint(panel, items):
    """Draw (points, fill, stroke, width) polygons back to front."""
    for pts, fill, stroke, width in sorted(items, key=lambda it: depth(it[0])):
        panel.polygon(pts, fill, stroke, width)


def force_colour(f, fmax):
    """Diverging: compression blue, tension red, near zero pale grey."""
    t = min(abs(f) / fmax, 1.0) ** 0.6
    end = (28, 126, 214) if f < 0 else (224, 49, 49)
    return hexcolor(lerp((222, 226, 230), end, t))


def draw_edges_by_force(panel, mesh, fmax, width=2.2):
    edges = sorted(mesh.edges(), key=lambda e: depth([xyz(mesh, e[0]), xyz(mesh, e[1])]))
    for u, v in edges:
        f = mesh.edge_attribute((u, v), "force")
        panel.line(xyz(mesh, u), xyz(mesh, v), force_colour(f, fmax), width)


def fig_app_form_finding():
    corner_net, corners = form_finding.corner_supported_net()
    edge_net, edge_fixed = form_finding.edge_supported_net()
    shell = form_finding.form_find(corner_net, corners)
    vault = form_finding.form_find(edge_net, edge_fixed)
    fig = Figure(900, 360)

    p = Panel(fig, 0, 0, 260, 360, all_points(corner_net), title="input: a flat net", pad=30)
    for u, v in corner_net.edges():
        stiff = corner_net.edge_attribute((u, v), "q")
        p.line(xyz(corner_net, u), xyz(corner_net, v), ORANGE if stiff else GREY, 3 if stiff else 1)
    for k in corners:
        p.dot(xyz(corner_net, k), 7, RED)
    fig.add(_text(130, 330, "red: fixed   orange: q = 6", 12, INK))
    fig.add(_text(130, 348, "grey: q = 1", 12, INK))

    pts = all_points(shell) + all_points(vault)
    for i, (mesh, title, note) in enumerate([
        (shell, "corners fixed", "the stiff edges arch inward in plan"),
        (vault, "whole boundary fixed", "a 'pillow' vault"),
    ]):
        x0 = 260 + i * 320
        p = Panel(fig, x0, 0, 320, 360, pts, view="iso", title=title, pad=24)
        fmax = max(abs(f) for f in mesh.edges_attribute("force"))
        paint(p, [([xyz(mesh, v) for v in mesh.face_vertices(f)], FACE, FACE, 0.5) for f in mesh.faces()])
        draw_edges_by_force(p, mesh, fmax, 1.6)
        rise = max(mesh.vertices_attribute("z"))
        fig.add(_text(x0 + 160, 330, f"rise {rise:.1f} m on a 10 m span -- {note}", 12, INK))
        fig.add(_text(x0 + 160, 348, "every edge in compression (blue)", 12, BLUE))
    fig.save("app-form-finding.svg")


def fig_app_structure():
    net, fixed = form_finding.edge_supported_net()
    vault = form_finding.form_find(net, fixed)
    rise = max(vault.vertices_attribute("z"))
    shapes = [
        ("the hanging net", form_finding.form_find(net, fixed, compression=False)),
        ("inverted: the vault", vault),
        ("a pyramid, same rise", structural_analysis.tent(net, rise)),
    ]
    results = []
    for title, shape in shapes:
        shape.quads_to_triangles()
        try:
            results.append((title, structural_analysis.analyse_truss(shape, fixed), None))
        except ValueError as error:
            results.append((title, shape, error))
    fmax = max(abs(f) for _, m, err in results if err is None for f in m.edges_attribute("force"))
    pts = [p for _, m, _ in results for p in all_points(m)]
    fig = Figure(900, 370)
    for i, (title, mesh, error) in enumerate(results):
        p = Panel(fig, i * 300, 0, 300, 370, pts, view="iso", title=title, pad=22)
        if error is None:
            draw_edges_by_force(p, mesh, fmax, 1.4)
            sm = structural_analysis.summary(mesh)
            share = sm["compression_share"]
            colour = BLUE if share > 0.5 else RED
            label = f"{share:.1%} of force is compression" if share > 0.5 else f"{1 - share:.1%} of force is tension"
            fig.add(_text(i * 300 + 150, 336, label, 13, colour, weight="bold"))
            fig.add(_text(i * 300 + 150, 356, f"max displacement {sm['max_displacement'] * 1000:.1f} mm", 12, INK))
        else:
            draw_edges(p, mesh, GREY, 1)
            fig.add(_text(i * 300 + 150, 336, "ValueError: the truss is a mechanism", 13, RED, weight="bold"))
            fig.add(_text(i * 300 + 150, 356, "flat facets cannot carry load without bending", 12, INK))
    fig.save("app-structure.svg")


def fig_app_scan():
    raw = scan_to_mesh.simulate_scan()
    clean, dropped = scan_to_mesh.remove_outliers(raw)
    untrimmed = scan_to_mesh.mesh_from_points(clean, max_edge=1e9)
    mesh = scan_to_mesh.mesh_from_points(clean)
    trimmed = mesh.copy()                 # before smoothing moves anything
    scan_to_mesh.smooth_heights(mesh)
    scan_to_mesh.deviation(mesh)
    fig = Figure(900, 380)

    p = Panel(fig, 0, 0, 300, 380, raw, view="iso", title="1. the scan: points, not surface", pad=20)
    for q in sorted(clean, key=lambda q: depth([q])):
        p.dot(q, 1.6, GREY, GREY)
    for q in dropped:
        p.dot(q, 4, RED)
    fig.add(_text(150, 350, f"{len(raw)} points; red: {len(dropped)} outliers removed", 12, INK))
    fig.add(_text(150, 368, "by comparing each point with its 8 neighbours", 12, INK))

    p = Panel(fig, 300, 0, 300, 380, clean, title="2. Delaunay mesh, trimmed (plan)", pad=20)
    def signature(m, f):          # a face, identified by its corner positions
        return tuple(sorted(tuple(round(c, 6) for c in m.vertex_coordinates(v)) for v in m.face_vertices(f)))

    kept = {signature(trimmed, f) for f in trimmed.faces()}
    for f in untrimmed.faces():
        tri = [untrimmed.vertex_coordinates(v) for v in untrimmed.face_vertices(f)]
        if signature(untrimmed, f) in kept:
            p.polygon(tri, FACE, BLUE, 0.4)
        else:
            p.polygon(tri, "#fff5f5", RED, 0.8)
    fig.add(_text(450, 350, "red: faces with an edge > 1.4 m, deleted", 12, RED))
    fig.add(_text(450, 368, f"result: euler = {mesh.euler()} -- exactly one hole, the rooflight", 12, INK))

    devs = mesh.vertices_attribute("deviation")
    worst = max(abs(d) for d in devs)
    p = Panel(fig, 600, 0, 300, 380, all_points(mesh), view="iso", title="3. deviation from design", pad=20)
    items = []
    for f in mesh.faces():
        vs = mesh.face_vertices(f)
        d = sum(mesh.vertex_attribute(v, "deviation") for v in vs) / len(vs)
        items.append(([xyz(mesh, v) for v in vs], force_colour(d, worst * 0.8), "none", 0))
    paint(p, items)
    rms = scan_to_mesh.rms(devs)
    fig.add(_text(750, 350, f"RMS {rms * 1000:.0f} mm after smoothing (scanner noise 30 mm)", 12, INK))
    fig.add(_text(750, 368, "blue: below design   red: above", 12, INK))
    fig.save("app-scan.svg")


def fig_app_cloth():
    start = cloth_simulation.cloth()
    _, frames = cloth_simulation.simulate(start, keep_every=40)
    picks = [frames[0], frames[1], frames[-1]]
    ball = Mesh.from_shape(Sphere(radius=0.98), u=24, v=16)
    pts = all_points(start) + all_points(frames[-1]) + all_points(ball)
    fig = Figure(900, 360)
    for i, (mesh, title) in enumerate(zip(picks, ["t = 0 s", "t = 0.67 s", "t = 4 s: at rest"])):
        p = Panel(fig, i * 300, 0, 300, 360, pts, view="iso", title=title, pad=20)
        items = []
        for f in ball.faces():
            n = ball.face_normal(f)
            if -n[0] - n[1] + n[2] <= 0:
                continue
            shade = 0.75 + 0.25 * max(0.0, (-0.35 * n[0] - 0.75 * n[1] + 0.56 * n[2]))
            items.append(([ball.vertex_coordinates(v) for v in ball.face_vertices(f)],
                          hexcolor([206 * shade, 212 * shade, 218 * shade]), "none", 0))
        for f in mesh.faces():
            items.append(([xyz(mesh, v) for v in mesh.face_vertices(f)], "#ffe8cc", ORANGE, 0.6))
        paint(p, items)
    s = cloth_simulation.stretch(frames[-1], start)
    fig.add(_text(450, 350, f"{start.number_of_vertices()} particles, {start.number_of_edges()} edge constraints; "
                  f"same topology throughout; worst edge stretch {s:.1%}", 12, INK))
    fig.save("app-cloth.svg")


# ----------------------------------------------------------------------------
# figures for the notebooks in ../notebooks (the README does not use these)
# ----------------------------------------------------------------------------
def _offset_arrow(panel, a, b, colour, off=0.1, width=2.2, shorten=0.22):
    """An arrow from a to b, pushed to its left: the side its face is on."""
    d = [b[0] - a[0], b[1] - a[1], 0]
    L = math.hypot(d[0], d[1])
    n = [-d[1] / L, d[0] / L, 0]
    A = [a[i] + n[i] * off for i in range(3)]
    B = [b[i] + n[i] * off for i in range(3)]
    panel.arrow(lerp(A, B, shorten), lerp(A, B, 1 - shorten), colour, width)
    return lerp(A, B, 0.5), n


def fig_walk():
    mesh = grid(2, 2)
    fig = Figure(900, 420)

    p = Panel(fig, 0, 0, 450, 400, all_points(mesh), pad=60, title="round a face: face_halfedges(0)")
    draw_faces(p, mesh, fill="white", stroke=GREY, width=1)
    draw_faces(p, mesh, faces=[0], stroke=GREY, width=1)
    for step, (u, v) in enumerate(mesh.face_halfedges(0), 1):
        mid, n = _offset_arrow(p, xyz(mesh, u), xyz(mesh, v), BLUE)
        p.label([mid[i] + n[i] * 0.13 for i in range(3)], step, 13, BLUE, 0, 5, weight="bold")
    p.fkey(mesh.face_centroid(0), 0)
    for v in mesh.vertices():
        p.key(xyz(mesh, v), v)
    first = mesh.face_halfedges(0)[0]
    fig.add(_text(225, 392, f"halfedge_after({first}) = {mesh.halfedge_after(first)}: "
                  "keep asking and you are back where you started", 12, INK))

    centre = 4
    p = Panel(fig, 450, 0, 450, 400, all_points(mesh), pad=60,
              title=f"round a vertex: vertex_neighbors({centre}, ordered=True)")
    draw_faces(p, mesh, fill="white", stroke=GREY, width=1)
    ring = mesh.vertex_neighbors(centre, ordered=True)
    faces = mesh.vertex_faces(centre, ordered=True)
    for f in faces:
        p.polygon([xyz(mesh, v) for v in mesh.face_vertices(f)], "#fff4e6", GREY, 1)
    for step, nbr in enumerate(ring, 1):
        a, b = xyz(mesh, centre), xyz(mesh, nbr)
        p.arrow(lerp(a, b, 0.14), lerp(a, b, 0.84), ORANGE, 2.4)
        p.label(lerp(a, b, 0.5), step, 13, ORANGE, 12, -8, weight="bold")
    for v in mesh.vertices():
        p.key(xyz(mesh, v), v, ORANGE if v == centre else INK)
    for f in faces:
        p.fkey(mesh.face_centroid(f), f, ORANGE)
    fig.add(_text(675, 392, f"neighbours in order {ring}; faces in order {faces}", 12, INK))
    fig.save("mesh-walk.svg")


def fig_measure():
    mesh = wave(grid(6, 4, 0.5), amplitude=0.7, wavelength=3.0)
    pts = all_points(mesh)
    fig = Figure(900, 360)

    p = Panel(fig, 0, 0, 450, 340, pts, view="iso", pad=44, title="where it is, which way it faces")
    paint(p, [([xyz(mesh, v) for v in mesh.face_vertices(f)], FACE, BLUE, 1) for f in mesh.faces()])
    for f in sorted(mesh.faces(), key=lambda f: depth([mesh.face_centroid(f)])):
        c, n = mesh.face_centroid(f), mesh.face_normal(f)
        p.arrow(c, [c[i] + 0.32 * n[i] for i in range(3)], ORANGE, 1.6, head=5)
        p.dot(c, 2.5, ORANGE)
    fig.add(_text(225, 348, "dot: face_centroid(f)    arrow: face_normal(f)", 12, INK))

    p = Panel(fig, 450, 0, 450, 340, pts, view="iso", pad=44, title="how big it is")
    areas = {f: mesh.face_area(f) for f in mesh.faces()}
    lo, hi = min(areas.values()), max(areas.values())
    paint(p, [([xyz(mesh, v) for v in mesh.face_vertices(f)], ramp((areas[f] - lo) / (hi - lo)), "white", 1)
              for f in mesh.faces()])
    fig.add(_text(675, 348, f"face_area(f): {lo:.3f} to {hi:.3f} m2 -- the plan squares are all 0.250 m2", 12, INK))
    fig.save("mesh-measure.svg")


def fig_operations():
    def counts(m):
        return f"V={m.number_of_vertices()} E={m.number_of_edges()} F={m.number_of_faces()}  euler={m.euler()}"

    base = grid(3, 3)
    tri = base.copy()
    tri.quads_to_triangles()
    hole = base.copy()
    hole.delete_face(4)
    fan = base.copy()
    new = fan.insert_vertex(4)
    cases = [("the grid", base, []), ("quads_to_triangles()", tri, []),
             ("delete_face(4)", hole, []), ("insert_vertex(4)", fan, [new])]
    fig = Figure(900, 300)
    for i, (title, mesh, marked) in enumerate(cases):
        p = Panel(fig, i * 225, 0, 225, 270, all_points(base), pad=26, title=title)
        draw_faces(p, mesh, stroke=BLUE, width=1.2)
        if title.startswith("delete"):
            p.polygon([xyz(base, v) for v in base.face_vertices(4)], "white", RED, 2)
        for v in mesh.vertices():
            p.dot(xyz(mesh, v), 5 if v in marked else 3, ORANGE if v in marked else INK)
        colour = RED if mesh.euler() != base.euler() else INK
        fig.add(_text(i * 225 + 112, 284, counts(mesh), 11, colour))
    fig.save("mesh-operations.svg")


def _canopy():
    """The canopy of notebook 05: 12 m x 8 m, an arch that is taller on one side."""
    mesh = Mesh()
    key = {}
    for j in range(7):
        for i in range(9):
            x, y = i * 1.5, j * 8 / 6
            key[i, j] = mesh.add_vertex(x=x, y=y, z=3.0 + (1.2 + 0.08 * (y - 4)) * math.sin(math.pi * x / 12))
    for j in range(6):
        for i in range(8):
            mesh.add_face([key[i, j], key[i + 1, j], key[i + 1, j + 1], key[i, j + 1]])
    return mesh


def _warp(mesh, f):
    """Distance between the two diagonals of a quad face."""
    from compas.geometry import Line, distance_line_line
    a, b, c, d = [xyz(mesh, v) for v in mesh.face_vertices(f)]
    return distance_line_line(Line(a, c), Line(b, d))


def fig_app_canopy():
    canopy = _canopy()
    fig = Figure(900, 380)

    # one quad, its warp exaggerated so that it can be seen
    quad = [[0, 0, 0], [2, 0, 0.75], [2, 2, 0], [0, 2, 0.75]]
    p = Panel(fig, 0, 0, 300, 340, quad + [[0, 0, -0.2]], view="iso", pad=46, title="a quad is not always flat")
    p.polygon(quad, FACE, BLUE, 1.5, 0.7)
    p.line(quad[0], quad[2], BLUE, 2.5)
    p.line(quad[1], quad[3], ORANGE, 2.5)
    m1, m2 = lerp(quad[0], quad[2], 0.5), lerp(quad[1], quad[3], 0.5)
    p.line(m1, m2, RED, 3)
    p.dot(m1, 4, BLUE)
    p.dot(m2, 4, ORANGE)
    p.label(m2, "warp", 13, RED, 14, 22, "start", "bold")
    for corner in quad:
        p.dot(corner, 4)
    fig.add(_text(150, 352, "the two diagonals miss each other;", 12, INK))
    fig.add(_text(150, 370, "the gap is what flat glass cannot follow", 12, INK))

    pts = all_points(canopy)
    warps = {f: _warp(canopy, f) for f in canopy.faces()}
    top = max(warps.values())
    p = Panel(fig, 300, 0, 300, 340, pts, view="iso", pad=24, title="warp of every panel")
    paint(p, [([xyz(canopy, v) for v in canopy.face_vertices(f)], ramp(warps[f] / top), "white", 1)
              for f in canopy.faces()])
    fig.add(_text(450, 352, f"{min(warps.values()) * 1000:.0f} to {top * 1000:.0f} mm:", 12, INK))
    fig.add(_text(450, 370, "least at the crown, most at the two ends", 12, INK))

    slope = {f: math.degrees(math.acos(min(1.0, abs(canopy.face_normal(f)[2])))) for f in canopy.faces()}
    lo, hi = min(slope.values()), max(slope.values())
    p = Panel(fig, 600, 0, 300, 340, pts, view="iso", pad=24, title="slope of every panel")
    paint(p, [([xyz(canopy, v) for v in canopy.face_vertices(f)], ramp((slope[f] - lo) / (hi - lo)), "white", 1)
              for f in canopy.faces()])
    fig.add(_text(750, 352, f"{lo:.0f} to {hi:.0f} degrees, read from face_normal:", 12, INK))
    fig.add(_text(750, 370, "blue panels are where rain is slow to leave", 12, INK))
    fig.save("app-canopy.svg")


def fig_app_patterns():
    cage = Mesh.from_meshgrid(dx=12, nx=3, dy=12, ny=3)
    for v in cage.vertices():
        cage.vertex_attribute(v, "z", 0.0 if cage.is_vertex_on_boundary(v) else 4.0)
    quads = cage.subdivided(k=2, scheme="catmullclark")
    triangles = quads.copy()
    triangles.quads_to_triangles()
    dual = triangles.dual()
    pts = all_points(quads)
    fig = Figure(900, 380)
    for i, (title, mesh, colour) in enumerate([("quads", quads, BLUE), ("triangles", triangles, GREEN),
                                               ("dual of the triangles", dual, ORANGE)]):
        p = Panel(fig, i * 300, 0, 300, 330, pts, view="iso", pad=20, title=title)
        paint(p, [([xyz(mesh, v) for v in mesh.face_vertices(f)], "white", colour, 1.1) for f in mesh.faces()])
        metres = sum(mesh.edge_length(e) for e in mesh.edges())
        busiest = max(mesh.vertex_degree(v) for v in mesh.vertices())
        fig.add(_text(i * 300 + 150, 346, f"{mesh.number_of_vertices()} nodes, {mesh.number_of_edges()} bars, "
                      f"{metres:.0f} m", 12, INK))
        fig.add(_text(i * 300 + 150, 366, f"up to {busiest} bars in one node", 12, colour, weight="bold"))
    fig.save("app-patterns.svg")


if __name__ == "__main__":
    fig_soup_vs_mesh()
    fig_anatomy()
    fig_winding()
    fig_halfedges()
    fig_neighbours()
    fig_boundary()
    fig_loops_strips()
    fig_attributes()
    fig_euler()
    fig_deform()
    fig_subdivide()
    fig_dual()
    fig_app_form_finding()
    fig_app_structure()
    fig_app_scan()
    fig_app_cloth()
    fig_walk()
    fig_measure()
    fig_operations()
    fig_app_canopy()
    fig_app_patterns()
