"""
Draw the timber figure of Week 09 Part A, from the script students run.

    uv run --extra timber Lecture/Lecture_09/figures/make_figures_timber.py

The SVG helpers are copied from Week 06, on purpose: each lecture folder stays
runnable on its own.
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "applications"))

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
    fig_app_timber()
