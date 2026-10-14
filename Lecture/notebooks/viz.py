"""
Small drawing helpers for the DCCG notebooks -- inline SVG, no matplotlib.

    from viz import draw_mesh, draw_graph, draw_plan, draw_points, chart, row

Every function returns a Figure. In Jupyter or VS Code, a Figure that is the
last line of a cell draws itself. Anywhere else (a plain terminal), call
fig.save("name.svg") and open the file.

This is a copy of the SVG writer behind the lecture figures
(Lecture/Lecture_05/figures/make_figures.py), plus a few one-call helpers.
It is deliberately small: read it if you want to know how a figure is made.
"""

import math
import pathlib

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

    def svg(self):
        body = "\n".join(self.items)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" '
            f'height="{self.height}" viewBox="0 0 {self.width} {self.height}" '
            'font-family="Helvetica, Arial, sans-serif">\n'
            f'<rect width="100%" height="100%" fill="white"/>\n{body}\n</svg>\n'
        )

    # Jupyter and VS Code call this to draw the figure inline
    def _repr_svg_(self):
        return self.svg()

    def __repr__(self):
        return f"<figure {self.width}x{self.height} -- in a plain REPL, call .save('name.svg') and open the file>"

    def save(self, path):
        """Write the figure to an .svg file (open it in a browser or in VS Code)."""
        pathlib.Path(path).write_text(self.svg())
        return path


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
# one-call helpers
# ----------------------------------------------------------------------------
CYCLE = [BLUE, ORANGE, GREEN, PURPLE, RED, "#f59f00", "#0ca678", "#d6336c", "#495057", "#74c0fc"]


def _hex(rgb):
    return "#%02x%02x%02x" % tuple(int(round(max(0, min(255, c)))) for c in rgb)


def ramp(t):
    """Blue -> purple -> orange for t in [0, 1]."""
    stops = [(28, 126, 214), (112, 72, 232), (232, 89, 12)]
    t = max(0.0, min(1.0, t))
    a, b, u = (stops[0], stops[1], t * 2) if t <= 0.5 else (stops[1], stops[2], (t - 0.5) * 2)
    return _hex([a[i] + (b[i] - a[i]) * u for i in range(3)])


def draw_mesh(mesh, title=None, view="plan", vertex_labels=True, face_labels=False,
              face_colors=None, highlight_vertices=(), highlight_faces=(), highlight_edges=(),
              size=(520, 380)):
    """Draw a COMPAS mesh. face_colors: {face: '#rrggbb'}; highlights are drawn in orange."""
    fig = Figure(*size)
    pts = [mesh.vertex_coordinates(v) for v in mesh.vertices()]
    p = Panel(fig, 0, 0, size[0], size[1], pts, view=view, title=title, pad=34)
    faces = list(mesh.faces())
    if view == "iso":
        faces.sort(key=lambda f: -sum(mesh.face_centroid(f)[:2]) + mesh.face_centroid(f)[2])
    for f in faces:
        fill = (face_colors or {}).get(f, "#ffe8cc" if f in highlight_faces else FACE)
        p.polygon([mesh.vertex_coordinates(v) for v in mesh.face_vertices(f)], fill, GREY if view == "plan" else BLUE, 1)
    for u, v in highlight_edges:
        p.line(mesh.vertex_coordinates(u), mesh.vertex_coordinates(v), ORANGE, 4)
    if face_labels:
        for f in mesh.faces():
            p.fkey(mesh.face_centroid(f), f, BLUE, 11)
    for v in mesh.vertices():
        hot = v in highlight_vertices
        if vertex_labels:
            p.key(mesh.vertex_coordinates(v), v, ORANGE if hot else INK, 9, 10)
        else:
            p.dot(mesh.vertex_coordinates(v), 4 if hot else 2.5, ORANGE if hot else INK)
    return fig


def draw_graph(graph, title=None, node_labels=True, node_colors=None, edge_colors=None,
               path=None, size=(520, 380)):
    """Draw a COMPAS Graph by its node x, y. path: a list of nodes drawn in orange."""
    fig = Figure(*size)
    pts = [graph.node_coordinates(n) for n in graph.nodes()]
    p = Panel(fig, 0, 0, size[0], size[1], pts, title=title, pad=40)
    on_path = set(zip(path, path[1:])) | set(zip(path[1:], path)) if path else set()
    for u, v in graph.edges():
        colour = (edge_colors or {}).get((u, v)) or (edge_colors or {}).get((v, u))
        if (u, v) in on_path:
            colour = ORANGE
        p.line(graph.node_coordinates(u), graph.node_coordinates(v), colour or GREY, 4 if (u, v) in on_path else 2)
    for n in graph.nodes():
        colour = (node_colors or {}).get(n, BLUE)
        if node_labels:
            x, y = p.map(graph.node_coordinates(n))
            w = 7.2 * len(str(n)) + 12
            fig.add(f'<rect x="{x - w / 2:.1f}" y="{y - 10:.1f}" width="{w:.1f}" height="20" rx="5" '
                    f'fill="white" stroke="{colour}" stroke-width="2"/>')
            fig.add(_text(x, y + 4.5, n, 12, colour, "middle", "bold"))
        else:
            p.dot(graph.node_coordinates(n), 5, colour)
    return fig


def draw_plan(rooms, title=None, fills=None, graph=None, edge_colors=None, notes=None, size=(640, 440)):
    """Draw a floor plan: rooms {name: (xmin, ymin, xmax, ymax)} as rectangles.

    fills: {name: '#rrggbb'}; notes: {name: text} written under the room name;
    graph: a COMPAS Graph drawn on top (nodes as dots, edge_colors as in draw_graph).
    """
    fig = Figure(*size)
    corners = [(x, y, 0) for x0, y0, x1, y1 in rooms.values() for x, y in ((x0, y0), (x1, y1))]
    p = Panel(fig, 0, 0, size[0], size[1], corners, title=title, pad=24)
    for name, (x0, y0, x1, y1) in rooms.items():
        p.polygon([(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)], (fills or {}).get(name, LIGHT), INK, 2,
                  0.6 if fills and name in fills else 1.0)
    if graph is not None:
        for u, v in graph.edges():
            colour = (edge_colors or {}).get((u, v)) or (edge_colors or {}).get((v, u)) or BLUE
            via = graph.edge_attribute((u, v), "door")
            stops = [graph.node_coordinates(u)] + ([via] if via else []) + [graph.node_coordinates(v)]
            for a, b in zip(stops, stops[1:]):
                p.line(a, b, colour, 4 if colour != BLUE else 2)
        for n in graph.nodes():
            p.dot(graph.node_coordinates(n), 4, BLUE)
    for name, (x0, y0, x1, y1) in rooms.items():
        centre = ((x0 + x1) / 2, (y0 + y1) / 2, 0)
        note = (notes or {}).get(name)
        if note and (y1 - y0) * p.s < 60:               # a low room: name and note on one line
            p.label(centre, f"{name}  {note}", 12, INK, 0, -8, "middle", "bold")
            continue
        p.label(centre, name, 12, INK, 0, -8, "middle", "bold")
        if note:
            p.label(centre, note, 11, INK, 0, 18)
    return fig


def draw_points(points, title=None, colors=None, polygons=(), polygon_fills=None, lines=(),
                labels=False, size=(520, 380), bounds=None):
    """Draw 2D points, optional polygons (lists of points) and lines ((a, b) pairs)."""
    fig = Figure(*size)
    frame = [list(q) + [0] * (3 - len(q)) for q in (bounds or points)]
    p = Panel(fig, 0, 0, size[0], size[1], frame, title=title, pad=24)
    for i, poly in enumerate(polygons):
        fill = (polygon_fills[i] if polygon_fills else FACE)
        p.polygon([list(q[:2]) + [0] for q in poly], fill, PURPLE, 1.2)
    for a, b in lines:
        p.line(list(a[:2]) + [0], list(b[:2]) + [0], GREY, 1.2)
    for i, q in enumerate(points):
        p.dot(list(q[:2]) + [0], 4, (colors[i] if colors else INK))
        if labels:
            p.label(list(q[:2]) + [0], i, 10, INK, 8, -6, "start")
    return fig


def chart(series, title=None, xlabel="", size=(520, 300)):
    """series: {label: [y0, y1, ...]} drawn against their index."""
    fig = Figure(*size)
    w, h, x0, y0 = size[0] - 90, size[1] - 80, 60, 40
    ys = [y for vals in series.values() for y in vals]
    lo, hi = min(ys), max(ys)
    hi = hi if hi > lo else lo + 1
    n = max(len(v) for v in series.values())
    if title:
        fig.add(_text(size[0] / 2, 22, title, 14, INK, weight="bold"))
    fig.add(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="white" stroke="{GREY}"/>')
    for k, (label, vals) in enumerate(series.items()):
        pts = [(x0 + w * i / max(1, n - 1), y0 + h - h * (v - lo) / (hi - lo)) for i, v in enumerate(vals)]
        fig.add('<polyline points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) +
                f'" fill="none" stroke="{CYCLE[k % len(CYCLE)]}" stroke-width="2.5"/>')
        fig.add(_text(x0 + w - 6, y0 + 16 + 16 * k, label, 11, CYCLE[k % len(CYCLE)], "end", "bold"))
    fig.add(_text(x0 - 6, y0 + 10, f"{hi:.3g}", 10, GREY, "end"))
    fig.add(_text(x0 - 6, y0 + h, f"{lo:.3g}", 10, GREY, "end"))
    fig.add(_text(x0 + w / 2, y0 + h + 22, xlabel, 11, INK))
    return fig


def row(*figures):
    """Place figures side by side in one figure."""
    out = Figure(sum(f.width for f in figures), max(f.height for f in figures))
    x = 0
    for f in figures:
        out.add(f'<g transform="translate({x},0)">')
        out.items.extend(f.items)
        out.add("</g>")
        x += f.width
    return out


# ----------------------------------------------------------------------------
# 3D, with compas_notebook (Jupyter in the browser; VS Code)
# ----------------------------------------------------------------------------
def _points_of(obj):
    """Some points that bound obj, for framing the camera."""
    if hasattr(obj, "vertices") and hasattr(obj, "vertex_coordinates"):       # Mesh
        return [obj.vertex_coordinates(v) for v in obj.vertices()]
    if hasattr(obj, "nodes") and hasattr(obj, "node_coordinates"):            # Graph
        return [obj.node_coordinates(n) for n in obj.nodes()]
    if hasattr(obj, "start") and hasattr(obj, "end"):                         # Line
        return [list(obj.start), list(obj.end)]
    if hasattr(obj, "points"):                                                # Box, Polyline, Polygon ...
        return [list(p) for p in obj.points]
    if hasattr(obj, "point") and hasattr(obj, "xaxis"):                       # Frame
        return [list(obj.point)]
    if hasattr(obj, "x") and hasattr(obj, "z"):                               # Point
        return [[obj.x, obj.y, obj.z]]
    return []


def _in_jupyter_kernel():
    try:
        from IPython import get_ipython
        shell = get_ipython()
        return shell is not None and hasattr(shell, "kernel")
    except ImportError:
        return False


def view3d(*items, width=900, height=460, top=False):
    """Show COMPAS objects in an interactive 3D view, framed on what you add.

        view3d(mesh)
        view3d((mesh, {"facecolor": colours}), frame, (graph, {"nodesize": 0.2}))

    Each item is a COMPAS geometry or datastructure, or (item, {options}) where
    options are the scene options of that object (facecolor, show_edges ...).
    Drag to orbit, scroll to zoom. Needs compas_notebook and a Jupyter front end
    (JupyterLab in the browser, or VS Code). Outside Jupyter (a plain script)
    it prints one line instead.
    """
    if not _in_jupyter_kernel():
        print(f"[3D view of {len(items)} object(s): open this notebook in JupyterLab or VS Code to see it]")
        return None
    from compas_notebook.config import Config, ViewConfig
    from compas_notebook.viewer import Viewer

    pairs = [it if isinstance(it, tuple) else (it, {}) for it in items]
    pts = [p for obj, _ in pairs for p in _points_of(obj)] or [[0, 0, 0]]
    lo = [min(p[i] for p in pts) for i in range(3)]
    hi = [max(p[i] for p in pts) for i in range(3)]
    centre = [(a + b) / 2 for a, b in zip(lo, hi)]
    size = max(max(b - a for a, b in zip(lo, hi)), 1e-3)

    config = Config()
    # a fresh ViewConfig per viewer: compas_notebook's Config shares one by default
    config.view = ViewConfig(viewport="top" if top else "perspective", width=width, height=height)
    config.view.camera.target = centre
    config.view.camera.position = ([centre[0], centre[1], centre[2] + 3 * size] if top else
                                   [centre[0] + 0.9 * size, centre[1] - 1.5 * size, centre[2] + 1.1 * size])
    viewer = Viewer(config=config)
    for obj, options in pairs:
        viewer.scene.add(obj, **options)
    viewer.show()
    return None
