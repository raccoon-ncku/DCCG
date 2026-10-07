"""
Draw every figure in the Week 06 README -- from real COMPAS graphs.

    uv run Lecture/Lecture_06/figures/make_figures.py

Same idea as Week 05's figures: nothing is hand-drawn. Each picture is built
with the Graph methods the README teaches, and the traversal orders, hop
counts and path lengths printed on the figures are computed, not typed.

The SVG-writing helpers below are a copy of the ones in
Lecture/Lecture_05/figures/make_figures.py. They are duplicated on purpose:
each lecture folder stays runnable on its own.
"""

import math
import random
from collections import deque
from pathlib import Path

from compas.datastructures import Graph, Mesh
from compas.topology import connected_components, dijkstra_path, shortest_path

HERE = Path(__file__).parent

# the application figures are drawn from the scripts students run
import sys  # noqa: E402

sys.path.insert(0, str(HERE.parent / "graph_applications"))
import plan_analysis  # noqa: E402
import street_network as streets  # noqa: E402  (street_network() is a helper below)

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


YELLOW = "#f59f00"
CYCLE = [BLUE, ORANGE, GREEN, PURPLE, RED, YELLOW, "#0ca678", "#d6336c"]


def lerp(a, b, t):
    return [a[i] + (b[i] - a[i]) * t for i in range(3)]


def hexcolor(rgb):
    return "#%02x%02x%02x" % tuple(int(round(c)) for c in rgb)


def ramp(t):
    """Blue -> purple -> orange, t in [0, 1]. Dark enough for white text."""
    stops = [(28, 126, 214), (112, 72, 232), (232, 89, 12)]
    if t <= 0.5:
        return hexcolor(lerp(stops[0], stops[1], t * 2))
    return hexcolor(lerp(stops[1], stops[2], (t - 0.5) * 2))


def pt(graph, n):
    return graph.node_coordinates(n)


def all_points(graph):
    return [pt(graph, n) for n in graph.nodes()]


def draw_graph(p, graph, color=INK, width=2, r=6, fill=INK, edges=None, nodes=None):
    for u, v in edges if edges is not None else graph.edges():
        p.line(pt(graph, u), pt(graph, v), color, width)
    for n in nodes if nodes is not None else graph.nodes():
        p.dot(pt(graph, n), r, fill)


def tag(p, xyz_, s, color=INK, size=12, pad=5):
    """A text label on a white rounded box, centred on a world point."""
    x, y = p.map(xyz_)
    w = 7.0 * len(str(s)) * size / 12 + 2 * pad
    h = size + 2 * pad
    p.fig.add(
        f'<rect x="{x - w / 2:.1f}" y="{y - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="5" fill="white" stroke="{color}" stroke-width="1.5"/>'
    )
    p.fig.add(_text(x, y + size * 0.36, s, size, color, "middle", "bold"))


# ----------------------------------------------------------------------------
# the data: a small apartment, the same one checkpoint 1 builds
# ----------------------------------------------------------------------------
ROOMS = {                 # name: (xmin, ymin, xmax, ymax), metres
    "entry": (0, 0, 3, 3),
    "living": (3, 0, 9, 5),
    "kitchen": (9, 0, 13, 5),
    "hall": (0, 3, 3, 9),
    "bed1": (3, 5, 7, 9),
    "bath": (7, 5, 9, 9),
    "bed2": (9, 5, 13, 9),
}
DOORS = [                 # (room, room, door width)
    ("entry", "living", 1.2),
    ("entry", "hall", 0.9),
    ("hall", "living", 0.9),
    ("living", "kitchen", 1.6),
    ("hall", "bed1", 0.8),
    ("living", "bath", 0.7),
    ("kitchen", "bed2", 0.8),
]


def apartment():
    graph = Graph()
    for name, (x0, y0, x1, y1) in ROOMS.items():
        graph.add_node(name, x=(x0 + x1) / 2, y=(y0 + y1) / 2, z=0,
                       area=(x1 - x0) * (y1 - y0))
    for a, b, width in DOORS:
        graph.add_edge(a, b, width=width)
    return graph


def door_point(a, b):
    """The middle of the wall two rooms share."""
    ax0, ay0, ax1, ay1 = ROOMS[a]
    bx0, by0, bx1, by1 = ROOMS[b]
    x0, x1 = max(ax0, bx0), min(ax1, bx1)
    y0, y1 = max(ay0, by0), min(ay1, by1)
    return [(x0 + x1) / 2, (y0 + y1) / 2, 0]


def bfs_hops(graph, start):
    hops = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nbr in graph.neighbors(node):
            if nbr not in hops:
                hops[nbr] = hops[node] + 1
                queue.append(nbr)
    return hops


def bfs_order(graph, start):
    order, seen, queue = [], {start}, deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nbr in sorted(graph.neighbors(node)):
            if nbr not in seen:
                seen.add(nbr)
                queue.append(nbr)
    return order


def dfs_order(graph, start):
    order, seen, stack = [], set(), [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        for nbr in sorted(graph.neighbors(node), reverse=True):
            if nbr not in seen:
                stack.append(nbr)
    return order


def geometric_graph(n, radius, seed):
    """Random points, joined when closer than `radius` (example 301)."""
    rnd = random.Random(seed)
    graph = Graph()
    for i in range(n):
        graph.add_node(i, x=rnd.uniform(0, 10), y=rnd.uniform(0, 6), z=0)
    nodes = list(graph.nodes())
    for i, u in enumerate(nodes):
        for v in nodes[i + 1:]:
            if math.dist(pt(graph, u), pt(graph, v)) < radius:
                graph.add_edge(u, v)
    return graph


# ----------------------------------------------------------------------------
# the figures
# ----------------------------------------------------------------------------
def fig_plan_to_graph():
    graph = apartment()
    corners = [[x, y, 0] for (x0, y0, x1, y1) in ROOMS.values() for x, y in ((x0, y0), (x1, y1))]
    fig = Figure(900, 360)

    p = Panel(fig, 0, 0, 450, 360, corners, title="A floor plan ...", pad=26)
    for name, (x0, y0, x1, y1) in ROOMS.items():
        p.polygon([[x0, y0, 0], [x1, y0, 0], [x1, y1, 0], [x0, y1, 0]], LIGHT, INK, 2)
        p.label([(x0 + x1) / 2, (y0 + y1) / 2, 0], name, 13, INK, 0, 4)
    for a, b, _ in DOORS:
        d = door_point(a, b)
        x, y = p.map(d)
        fig.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="white" stroke="{ORANGE}" stroke-width="3"/>')

    p = Panel(fig, 450, 0, 450, 360, corners, title="... is a graph: rooms are nodes, doors are edges", pad=26)
    for name, (x0, y0, x1, y1) in ROOMS.items():
        p.polygon([[x0, y0, 0], [x1, y0, 0], [x1, y1, 0], [x0, y1, 0]], "white", "#dee2e6", 1.5)
    for u, v in graph.edges():
        p.line(pt(graph, u), door_point(u, v), ORANGE, 3)
        p.line(door_point(u, v), pt(graph, v), ORANGE, 3)
    for n in graph.nodes():
        tag(p, pt(graph, n), n, BLUE)
    fig.save("graph-plan.svg")


def fig_anatomy():
    graph = apartment()
    fig = Figure(900, 380)
    p = Panel(fig, 0, 0, 560, 380, all_points(graph), pad=50,
              title=f"{graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    for u, v in graph.edges():
        p.line(pt(graph, u), pt(graph, v), ORANGE, 3)
        mid = lerp(pt(graph, u), pt(graph, v), 0.5)
        tag(p, mid, f'{graph.edge_attribute((u, v), "width")} m', ORANGE, 10, 3)
    for n in graph.nodes():
        tag(p, pt(graph, n), n, BLUE)
    lines = [
        ('graph.node_attributes("living")', BLUE, "bold"),
        ("{", INK, "normal"),
        ('  "x": 6.0, "y": 2.5, "z": 0.0,', INK, "normal"),
        (f'  "area": {graph.node_attribute("living", "area"):.1f}', INK, "normal"),
        ("}", INK, "normal"),
        ("", INK, "normal"),
        ('graph.edge_attributes(("entry", "living"))', ORANGE, "bold"),
        ('{"width": 1.2}', INK, "normal"),
        ("", INK, "normal"),
        ('graph.neighbors("living")', INK, "bold"),
        (str(sorted(graph.neighbors("living"))), INK, "normal"),
        ('graph.degree("living")', INK, "bold"),
        (str(graph.degree("living")), INK, "normal"),
    ]
    for i, (s, c, w) in enumerate(lines):
        fig.add(_text(575, 70 + i * 22, s, 13, c, "start", w))
    fig.save("graph-anatomy.svg")


def fig_mesh_is_graph():
    mesh = Mesh.from_meshgrid(dx=4, nx=4, dy=3, ny=3)
    graph = Graph()
    for v in mesh.vertices():
        x, y, z = mesh.vertex_coordinates(v)
        graph.add_node(v, x=x, y=y, z=z)
    for u, v in mesh.edges():
        graph.add_edge(u, v)
    fig = Figure(900, 350)
    pts = all_points(graph)
    p = Panel(fig, 0, 0, 450, 330, pts, title="Mesh: vertices, edges, faces", pad=30)
    for f in mesh.faces():
        p.polygon([mesh.vertex_coordinates(v) for v in mesh.face_vertices(f)], FACE, BLUE, 1.5)
    draw_graph(p, graph, BLUE, 1.5, 4, BLUE)
    p = Panel(fig, 450, 0, 450, 330, pts, title="Graph: nodes and edges -- no faces", pad=30)
    draw_graph(p, graph, INK, 2, 5, INK)
    fig.add(_text(450, 338, f"mesh: V={mesh.number_of_vertices()} E={mesh.number_of_edges()} F={mesh.number_of_faces()}"
                  f"    graph: nodes={graph.number_of_nodes()} edges={graph.number_of_edges()}", 13, INK))
    fig.save("graph-mesh-is-graph.svg")


def fig_degree():
    graph = apartment()
    fig = Figure(900, 390)
    p = Panel(fig, 0, 0, 900, 360, all_points(graph), pad=60,
              title="graph.degree(node): how many edges meet there")
    draw_graph(p, graph, GREY, 3, 0, GREY)
    leaves = set(graph.leaves())
    for n in graph.nodes():
        d = graph.degree(n)
        color = RED if n in leaves else BLUE
        x, y = p.map(pt(graph, n))
        r = 12 + 5 * d
        fig.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" fill-opacity="0.18" stroke="{color}" stroke-width="2"/>')
        fig.add(_text(x, y + 5, str(d), 15, color, "middle", "bold"))
        fig.add(_text(x, y + r + 15, n, 12, INK))
    fig.add(_text(450, 378, f"red: graph.leaves() = {sorted(leaves)} -- degree 1, dead ends", 13, RED))
    fig.save("graph-degree.svg")


def fig_bfs():
    # a street grid with a few blocks merged (missing edges)
    graph = Graph()
    nx, ny = 7, 5
    for j in range(ny):
        for i in range(nx):
            graph.add_node(j * nx + i, x=i, y=j, z=0)
    missing = {(8, 9), (15, 16), (16, 23), (10, 17), (19, 26), (25, 26), (11, 12), (30, 31)}
    for j in range(ny):
        for i in range(nx):
            n = j * nx + i
            for m in ([n + 1] if i < nx - 1 else []) + ([n + nx] if j < ny - 1 else []):
                if (n, m) not in missing:
                    graph.add_edge(n, m)
    start = 0
    hops = bfs_hops(graph, start)
    top = max(hops.values())
    fig = Figure(900, 400)
    p = Panel(fig, 0, 0, 900, 400, all_points(graph), pad=40,
              title="Breadth-first search from the corner: rings of equal hop count")
    draw_graph(p, graph, GREY, 2, 0, GREY)
    for n in graph.nodes():
        c = ramp(hops[n] / top)
        p.key(pt(graph, n), hops[n], c, 13, 12)
    x, y = p.map(pt(graph, start))
    fig.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="18" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    fig.add(_text(450, 390, "the number on each node is its distance in hops; "
                  "gaps in the grid force the search around them", 13, INK))
    fig.save("graph-bfs.svg")


def fig_bfs_vs_dfs():
    graph = apartment()
    fig = Figure(900, 360)
    for i, (title, order, color) in enumerate([
        ("breadth-first from entry: near rooms first", bfs_order(graph, "entry"), BLUE),
        ("depth-first from entry: one corridor to the end", dfs_order(graph, "entry"), PURPLE),
    ]):
        p = Panel(fig, i * 450, 0, 450, 360, all_points(graph), title=title, pad=46)
        draw_graph(p, graph, GREY, 2.5, 0, GREY)
        for k, n in enumerate(order):
            p.key(pt(graph, n), k + 1, color, 13, 13)
            p.label(pt(graph, n), n, 11, INK, 0, 28)
        fig.add(_text(i * 450 + 225, 348, " → ".join(order), 11, color))
    fig.save("graph-bfs-vs-dfs.svg")


def street_network():
    """A street grid, plus a ring road that reaches far with few edges."""
    graph = Graph()
    nx, ny = 8, 3
    for j in range(ny):
        for i in range(nx):
            graph.add_node(f"{i},{j}", x=i, y=j, z=0)
    for j in range(ny):
        for i in range(nx):
            if i < nx - 1:
                graph.add_edge(f"{i},{j}", f"{i + 1},{j}")
            if j < ny - 1:
                graph.add_edge(f"{i},{j}", f"{i},{j + 1}")
    graph.add_node("ring", x=3.5, y=6.0, z=0)
    graph.add_edge("0,1", "ring")
    graph.add_edge("ring", "7,1")
    return graph, "0,1", "7,1"


def fig_shortest_paths():
    graph, start, goal = street_network()
    hop_path = shortest_path(graph.adjacency, start, goal)    # breadth-first
    short_path = graph.shortest_path(start, goal)              # A*, by length
    weight = {}
    for u, v in graph.edges():
        weight[u, v] = weight[v, u] = graph.edge_length((u, v))
    assert short_path == dijkstra_path(graph.adjacency, weight, start, goal)

    def length(path):
        return sum(graph.edge_length((a, b)) for a, b in zip(path, path[1:]))

    fig = Figure(900, 360)
    for i, (title, path, color) in enumerate([
        ("compas.topology.shortest_path(adjacency, a, b)", hop_path, ORANGE),
        ("graph.shortest_path(a, b)", short_path, GREEN),
    ]):
        p = Panel(fig, i * 450, 0, 450, 360, all_points(graph), title=title, pad=30)
        draw_graph(p, graph, "#ced4da", 2, 3.5, GREY)
        for a, b in zip(path, path[1:]):
            p.line(pt(graph, a), pt(graph, b), color, 4.5)
        for n in path:
            p.dot(pt(graph, n), 5.5, color)
        p.key(pt(graph, start), "a", INK, 11, 12)
        p.key(pt(graph, goal), "b", INK, 11, 12)
        fig.add(_text(i * 450 + 225, 348, f"{len(path) - 1} edges, length {length(path):.1f}",
                      14, color, weight="bold"))
    fig.save("graph-shortest-paths.svg")


def fig_components():
    graph = geometric_graph(60, 1.25, 7)
    parts = sorted(connected_components(graph.adjacency), key=len, reverse=True)
    fig = Figure(900, 360)
    p = Panel(fig, 0, 0, 900, 360, all_points(graph), pad=30,
              title=f"connected_components(graph.adjacency): {len(parts)} islands")
    for k, part in enumerate(parts):
        color = CYCLE[k % len(CYCLE)] if len(part) > 1 else GREY
        part = set(part)
        edges = [(u, v) for u, v in graph.edges() if u in part]
        draw_graph(p, graph, color, 2.5, 5, color, edges=edges, nodes=part)
    sizes = ", ".join(str(len(c)) for c in parts)
    fig.add(_text(450, 350, f"sizes: {sizes}  -- grey nodes have no edges at all", 12, INK))
    fig.save("graph-components.svg")


def brick_wall(courses=6, length=8, brick=1.0, height=0.5):
    """A running-bond wall: each course offset by half a brick."""
    graph = Graph()
    for c in range(courses):
        x = -0.5 * brick if c % 2 else 0.0
        while x < length - 1e-9:
            x0, x1 = max(x, 0.0), min(x + brick, length)
            graph.add_node(len(graph.node), x=(x0 + x1) / 2, y=c * height + height / 2, z=0,
                           course=c, x0=x0, x1=x1)
            x += brick
    nodes = list(graph.nodes())
    for u in nodes:
        cu, a0, a1 = (graph.node_attribute(u, k) for k in ("course", "x0", "x1"))
        for v in nodes:
            if v <= u:
                continue
            cv, b0, b1 = (graph.node_attribute(v, k) for k in ("course", "x0", "x1"))
            same = cu == cv and (abs(a1 - b0) < 1e-9 or abs(b1 - a0) < 1e-9)
            stacked = abs(cu - cv) == 1 and min(a1, b1) - max(a0, b0) > 1e-9
            if same or stacked:
                graph.add_edge(u, v, contact="head" if same else "bed")
    return graph, height


def fig_brick_wall():
    graph, h = brick_wall()
    top = max(graph.nodes(), key=lambda n: (graph.node_attribute(n, "course"), -abs(pt(graph, n)[0] - 4.2)))
    # every brick that the top brick rests on, all the way down: follow BED
    # joints downward only
    below = {top}
    frontier = [top]
    while frontier:
        n = frontier.pop()
        for m in graph.neighbors(n):
            if graph.node_attribute(m, "course") == graph.node_attribute(n, "course") - 1 and m not in below:
                below.add(m)
                frontier.append(m)
    corners = [[graph.node_attribute(n, "x0"), pt(graph, n)[1] - h / 2, 0] for n in graph.nodes()] + \
              [[graph.node_attribute(n, "x1"), pt(graph, n)[1] + h / 2, 0] for n in graph.nodes()]
    fig = Figure(900, 380)
    for i, title in enumerate(["bricks = nodes, joints = edges", "everything the marked brick rests on"]):
        p = Panel(fig, i * 450, 0, 450, 380, corners, title=title, pad=26)
        for n in graph.nodes():
            x0, x1 = graph.node_attribute(n, "x0"), graph.node_attribute(n, "x1")
            y = pt(graph, n)[1]
            fill = "#ffe8cc" if (i == 1 and n in below) else LIGHT
            g = 0.03
            p.polygon([[x0 + g, y - h / 2 + g, 0], [x1 - g, y - h / 2 + g, 0],
                       [x1 - g, y + h / 2 - g, 0], [x0 + g, y + h / 2 - g, 0]], fill, GREY, 1)
        if i == 0:
            for u, v in graph.edges():
                c = BLUE if graph.edge_attribute((u, v), "contact") == "bed" else ORANGE
                p.line(pt(graph, u), pt(graph, v), c, 1.8)
            for n in graph.nodes():
                p.dot(pt(graph, n), 3.5, INK)
        else:
            for u, v in graph.edges():
                if u in below and v in below and graph.edge_attribute((u, v), "contact") == "bed":
                    p.line(pt(graph, u), pt(graph, v), ORANGE, 3)
            for n in below:
                p.dot(pt(graph, n), 4, ORANGE)
            p.key(pt(graph, top), "★", INK, 10, 11)
    fig.add(_text(225, 370, "blue: bed joints (course to course)   orange: head joints (side by side)", 11, INK))
    fig.add(_text(675, 370, f"{len(below) - 1} bricks below carry the marked one -- a traversal, not a search by position", 11, INK))
    fig.save("graph-brick-wall.svg")


# ----------------------------------------------------------------------------
# two graphs of one frame, and the tree BFS leaves behind
# ----------------------------------------------------------------------------
FRAME = {                     # a portal frame with two knee braces (metres)
    "beam": ([0, 3, 0], [4, 3, 0]),
    "post_L": ([0, 0, 0], [0, 3, 0]),
    "post_R": ([4, 0, 0], [4, 3, 0]),
    "knee_L": ([0, 1.8, 0], [1.2, 3, 0]),
    "knee_R": ([4, 1.8, 0], [2.8, 3, 0]),
}


def _on_segment(p, a, b, tol=1e-9):
    cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    if abs(cross) > tol:
        return False
    dot = (p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])
    return -tol <= dot <= (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + tol


def frame_joints(frame=FRAME):
    """{(element, element): joint point} -- where an end of one lies on the other."""
    joints = {}
    names = list(frame)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            for end in frame[a]:
                if _on_segment(end, *frame[b]):
                    joints[a, b] = end
            for end in frame[b]:
                if _on_segment(end, *frame[a]):
                    joints[a, b] = end
    return joints


def element_graph(frame=FRAME):
    """Nodes = ELEMENTS (at their midpoints), edges = JOINTS."""
    g = Graph()
    for name, (a, b) in frame.items():
        g.add_node(name, x=(a[0] + b[0]) / 2, y=(a[1] + b[1]) / 2, z=0)
    for (a, b), point in frame_joints(frame).items():
        g.add_edge(a, b, point=point)
    return g


def bar_graph(frame=FRAME):
    """Nodes = POINTS (joints and free ends), edges = BAR SEGMENTS between them."""
    points = []
    for a, b in frame.values():
        points += [a, b]
    points += list(frame_joints(frame).values())
    unique = []
    for p in points:
        if not any(math.dist(p, q) < 1e-9 for q in unique):
            unique.append(p)
    g = Graph()
    for i, p in enumerate(unique):
        g.add_node(i, x=p[0], y=p[1], z=0)
    for name, (a, b) in frame.items():
        on = sorted((i for i, p in enumerate(unique) if _on_segment(p, a, b)),
                    key=lambda i: math.dist(unique[i], a))
        for u, v in zip(on, on[1:]):
            g.add_edge(u, v, element=name)
    return g


def fig_two_graphs():
    eg, bg = element_graph(), bar_graph()
    pts = [p for seg in FRAME.values() for p in seg]
    colours = {"beam": BLUE, "post_L": ORANGE, "post_R": ORANGE, "knee_L": GREEN, "knee_R": GREEN}
    fig = Figure(900, 380)

    p = Panel(fig, 0, 0, 300, 380, pts, title="a frame: five elements", pad=40)
    for name, (a, b) in FRAME.items():
        p.line(a, b, colours[name], 9, opacity=0.35)
        p.label(lerp(a, b, 0.5), name, 11, INK, 0, -10 if name in ("beam",) else 4,
                "middle", "bold")

    p = Panel(fig, 300, 0, 300, 380, pts, title="element graph: node = element", pad=40)
    for name, (a, b) in FRAME.items():
        p.line(a, b, colours[name], 9, opacity=0.12)
    for u, v in eg.edges():
        p.line(pt(eg, u), pt(eg, v), INK, 2)
    for n in eg.nodes():
        p.key(pt(eg, n), "", colours[n], 9, 1)
    fig.add(_text(450, 350, f"{eg.number_of_nodes()} nodes, {eg.number_of_edges()} edges: an edge IS a joint", 12, INK, weight="bold"))
    fig.add(_text(450, 368, "-> joinery, assembly order, compas_timber, BTLx", 12, INK))

    p = Panel(fig, 600, 0, 300, 380, pts, title="bar graph: node = point", pad=40)
    for u, v in bg.edges():
        p.line(pt(bg, u), pt(bg, v), colours[bg.edge_attribute((u, v), "element")], 3)
    for n in bg.nodes():
        p.dot(pt(bg, n), 5, INK)
    fig.add(_text(750, 350, f"{bg.number_of_nodes()} nodes, {bg.number_of_edges()} edges: a joint is a NODE", 12, INK, weight="bold"))
    fig.add(_text(750, 368, "-> structural analysis (W05 truss), meshes", 12, INK))
    fig.save("graph-two-graphs.svg")


def bfs_tree(graph, start):
    """{node: parent} -- the tree a breadth-first search leaves behind."""
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nbr in sorted(graph.neighbors(node)):
            if nbr not in parent:
                parent[nbr] = node
                queue.append(nbr)
    return parent


def fig_bfs_tree():
    graph = apartment()
    parent = bfs_tree(graph, "entry")
    tree = {(c, p) for c, p in parent.items() if p is not None}
    fig = Figure(900, 360)
    p = Panel(fig, 0, 0, 520, 360, all_points(graph), title="the tree a BFS from the entry leaves behind", pad=46)
    for u, v in graph.edges():
        if (u, v) in tree or (v, u) in tree:
            continue
        p.line(pt(graph, u), pt(graph, v), GREY, 2, dash="6,5")
    for child, par in tree:
        a, b = pt(graph, par), pt(graph, child)
        p.arrow(lerp(a, b, 0.12), lerp(a, b, 0.82), BLUE, 3, head=10)
    for n in graph.nodes():
        tag(p, pt(graph, n), n, INK if n == "entry" else BLUE)
    lines = [
        ("parent = {", INK, "bold"),
    ] + [(f'  "{c}": ' + ("None," if par is None else f'"{par}",'), INK, "normal") for c, par in parent.items()] + [
        ("}", INK, "bold"),
        ("", INK, "normal"),
        (f"{graph.number_of_nodes()} nodes, {len(tree)} tree edges (n - 1)", BLUE, "bold"),
        (f"{graph.number_of_edges() - len(tree)} dashed edge closes the loop", GREY, "bold"),
        ("", INK, "normal"),
        ("route to bed1: follow parents back", INK, "normal"),
        ("bed1 -> hall -> entry, then reverse", INK, "normal"),
    ]
    for i, (text, colour, weight) in enumerate(lines):
        fig.add(_text(560, 60 + i * 21, text, 13, colour, "start", weight))
    fig.save("graph-bfs-tree.svg")


# ----------------------------------------------------------------------------
# applications (section 11) -- drawn from ../graph_applications/*.py
# ----------------------------------------------------------------------------
def rect(r):
    x0, y0, x1, y1 = r
    return [[x0, y0, 0], [x1, y0, 0], [x1, y1, 0], [x0, y1, 0]]


def fig_app_plan():
    graph = plan_analysis.plan_graph()
    integ = plan_analysis.integration(graph)
    escape = plan_analysis.escape_distance(graph)
    critical = plan_analysis.critical_doors(graph)
    corners = [c for r in plan_analysis.ROOMS.values() for c in rect(r)]
    lo, hi = min(integ.values()), max(integ.values())
    limit = 25.0
    fig = Figure(900, 400)

    p = Panel(fig, 0, 0, 450, 380, corners, title="integration: how few doors to everywhere", pad=22)
    for name, r in plan_analysis.ROOMS.items():
        p.polygon(rect(r), ramp((integ[name] - lo) / (hi - lo)), "white", 2)
    for u, v in graph.edges():
        p.dot(graph.edge_attribute((u, v), "door"), 3.5, "white", INK)
    for name in plan_analysis.ROOMS:
        p.label(pt(graph, name), name, 11, "white", 0, 0, weight="bold")
        p.label(pt(graph, name), f"{integ[name]:.2f}", 10, "white", 0, 14)
    fig.add(_text(225, 392, "orange: integrated (where people pass)   blue: segregated (deep, private)", 11, INK))

    p = Panel(fig, 450, 0, 450, 380, corners, title="escape distance and critical doors", pad=22)
    for name, r in plan_analysis.ROOMS.items():
        over = escape[name] > limit
        p.polygon(rect(r), "#ffe3e3" if over else LIGHT, RED if over else "white", 3 if over else 2)
        p.label(pt(graph, name), f"{escape[name]:.1f} m", 11, RED if over else INK, 0, 4, weight="bold")
    for name in plan_analysis.EXITS:
        p.label(pt(graph, name), "EXIT", 10, GREEN, 0, 20, weight="bold")
    for u, v in graph.edges():
        d = graph.edge_attribute((u, v), "door")
        crit = (u, v) in critical or (v, u) in critical
        p.dot(d, 6 if crit else 3.5, RED if crit else GREY, "white")
    fig.add(_text(675, 392, f"red room: over {limit:.0f} m to the nearest exit   red dot: a door whose loss cuts rooms off", 11, INK))
    fig.save("app-plan.svg")


def fig_app_streets():
    cases = [("both bridges open", streets.town()),
             ("west bridge closed", streets.town(bridges=(7,)))]
    results = [(t, g, streets.street_betweenness(g)) for t, g in cases]
    top = max(max(eb.values()) for _, _, eb in results)
    def load(t):                        # pale grey -> purple -> orange
        if t < 0.5:
            return hexcolor(lerp((206, 212, 218), (112, 72, 232), t * 2))
        return hexcolor(lerp((112, 72, 232), (232, 89, 12), (t - 0.5) * 2))

    fig = Figure(900, 400)
    for i, (title, g, eb) in enumerate(results):
        p = Panel(fig, i * 450, 0, 450, 380, all_points(g), title=title, pad=26)
        r0 = streets.RIVER_ROW
        p.polygon([[-0.5, r0 + 0.12, 0], [9.5, r0 + 0.12, 0], [9.5, r0 + 0.48, 0], [-0.5, r0 + 0.48, 0]],
                  "#d0ebff", "#d0ebff", 1)
        for edge in sorted(eb, key=eb.get):
            t = eb[edge] / top
            p.line(pt(g, edge[0]), pt(g, edge[1]), load(t), 1.5 + 9 * t)
        busiest = max(eb, key=eb.get)
        trip = streets.average_trip(g)
        fig.add(_text(i * 450 + 225, 374, f"busiest: the bridge, carrying {eb[busiest]:.0%} of all shortest routes",
                      12, INK, weight="bold"))
        fig.add(_text(i * 450 + 225, 392, f"average trip {trip:.2f} blocks", 12, INK))
    fig.save("app-streets.svg")


def fig_app_timber():
    try:
        import timber_frame
    except ImportError:
        print("skipped app-timber.svg -- run with: uv run --extra timber ...")
        return
    from compas_timber.connections import JointTopology

    model, report = timber_frame.build_model(timber_frame.stud_wall())
    beams = {b.name: b for b in model.beams}

    def elev(p3):                       # elevation: x right, z up
        return [p3[0], p3[2], 0.0]

    pts = [elev(b.centerline.start) for b in beams.values()] + [elev(b.centerline.end) for b in beams.values()]
    colours = {JointTopology.TOPO_L: ORANGE, JointTopology.TOPO_T: BLUE, JointTopology.TOPO_X: RED}
    fig = Figure(900, 400)

    p = Panel(fig, 0, 0, 470, 380, pts, title="the wall: beams and the joints between them", pad=30)
    for b in beams.values():
        a, c = elev(b.centerline.start), elev(b.centerline.end)
        d = [c[0] - a[0], c[1] - a[1]]
        L = math.hypot(*d)
        n = [-d[1] / L * b.width / 2, d[0] / L * b.width / 2]
        p.polygon([[a[0] + n[0], a[1] + n[1], 0], [c[0] + n[0], c[1] + n[1], 0],
                   [c[0] - n[0], c[1] - n[1], 0], [a[0] - n[0], a[1] - n[1], 0]], "#f4e3c1", "#b08850", 1)
    for joint in model.joints:
        topo = JointTopology.TOPO_L if type(joint).__name__.startswith("L") else JointTopology.TOPO_T
        p.dot(elev(joint.location), 5, colours[topo])
    for cand in model.joint_candidates:
        if cand.topology == JointTopology.TOPO_X:
            p.dot(elev(cand.location), 8, RED)
            p.label(elev(cand.location), "X: needs Rhino", 11, RED, 10, -10, "start", "bold")

    import networkx as nx

    nxg = nx.Graph([tuple(e.name for e in c.elements) for c in model.joint_candidates])
    layout = nx.kamada_kawai_layout(nxg)
    mids = {name: [float(layout[name][0]), float(layout[name][1]), 0.0] for name in beams}
    p = Panel(fig, 470, 0, 430, 380, list(mids.values()), title="the same model as a graph (model.graph)", pad=40)
    for cand in model.joint_candidates:
        a, b = (e.name for e in cand.elements)
        colour = colours.get(cand.topology, GREY)
        p.line(mids[a], mids[b], colour, 2.5 if cand.topology == JointTopology.TOPO_X else 1.8,
               dash="5,4" if cand.topology == JointTopology.TOPO_X else None)
    for name, m in mids.items():
        deg = len(model.get_joints_for_element(beams[name]))
        p.dot(m, 3 + deg, INK)
        short = name.replace("_plate", "").replace("cripple_", "c").replace("_low", "↓").replace("_high", "↑")
        p.label(m, short, 9, INK, 0, -9 - deg)
    nodes, edges = report["graph"]
    fig.add(_text(110, 374, "● L joint (butt)", 12, ORANGE, "start"))
    fig.add(_text(220, 374, "● T joint (butt)", 12, BLUE, "start"))
    fig.add(_text(330, 374, "● X crossing", 12, RED, "start"))
    fig.add(_text(685, 356, f"{nodes} nodes (beams), {edges} edges (26 joints + 1 open X); size = degree", 12, INK))
    btlx = report["joints"]
    fig.add(_text(685, 374, f"{sum(btlx.values())} joints -> 33 JackRafterCuts in the BTLx file", 12, INK))
    fig.save("app-timber.svg")


if __name__ == "__main__":
    fig_plan_to_graph()
    fig_anatomy()
    fig_mesh_is_graph()
    fig_degree()
    fig_bfs()
    fig_bfs_vs_dfs()
    fig_shortest_paths()
    fig_components()
    fig_brick_wall()
    fig_two_graphs()
    fig_bfs_tree()
    fig_app_plan()
    fig_app_streets()
    fig_app_timber()
