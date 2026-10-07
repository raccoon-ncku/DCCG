"""
Draw every figure in the Simulation README -- by running the tutorials.

    uv run Lecture/Algorithms/simulation/figures/make_figures.py

The SVG helpers are a copy of Lecture/Lecture_05/figures/make_figures.py
(each folder stays runnable on its own).
"""

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "tutorials"))
import boids  # noqa: E402
import cellular_automata as ca  # noqa: E402
import dla  # noqa: E402

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



def lerp(a, b, t):
    return [a[i] + (b[i] - a[i]) * t for i in range(len(a))]


def hexcolor(rgb):
    return "#%02x%02x%02x" % tuple(int(round(max(0, min(255, c)))) for c in rgb)


def ramp(t):
    stops = [(28, 126, 214), (112, 72, 232), (232, 89, 12)]
    t = max(0.0, min(1.0, t))
    return hexcolor(lerp(stops[0], stops[1], t * 2)) if t <= 0.5 else hexcolor(lerp(stops[1], stops[2], (t - 0.5) * 2))


def square(p, x, y, d, fill, stroke="white"):
    p.polygon([[x, y, 0], [x + d, y, 0], [x + d, y + d, 0], [x, y + d, 0]], fill, stroke, 0.6)


def fig_life():
    g = np.zeros((7, 7), bool)
    g[1:4, 1:4] = ca.pattern([".#.", "..#", "###"])
    hist = ca.run(g, 4)
    fig = Figure(900, 380)
    for t, grid in enumerate(hist):
        p = Panel(fig, 10 + t * 92, 30, 90, 150, [[0, 0, 0], [7, 7, 0]], title=f"gen {t}", pad=6)
        for y in range(7):
            for x in range(7):
                square(p, x, 6 - y, 1, BLUE if grid[y, x] else LIGHT)
    fig.add(_text(240, 205, "a glider: after 4 generations, the same shape one cell down-right", 12, INK))
    fig.add(_text(240, 223, "nobody wrote 'move diagonally' -- only B3/S23", 12, INK, weight="bold"))
    # a CA tower: R-pentomino, generations stacked as floors
    seed = np.zeros((24, 24), bool)
    seed[10:13, 10:13] = ca.pattern([".##", "##.", ".#."])
    hist = ca.run(seed, 22)
    vox = ca.voxels(hist)
    pts = [[x, y, z * 0.9] for x, y, z in vox]
    p = Panel(fig, 470, 0, 430, 380, pts + [[0, 0, 0], [24, 24, 0]], view="iso", title="stack the generations: a 2D rule grows a tower", pad=24)
    order = sorted(vox, key=lambda v: (v[2], -(v[0] + v[1])))
    for x, y, z in order:
        h = z * 0.9
        top = [[x, y, h + 0.9], [x + 1, y, h + 0.9], [x + 1, y + 1, h + 0.9], [x, y + 1, h + 0.9]]
        front = [[x, y, h], [x + 1, y, h], [x + 1, y, h + 0.9], [x, y, h + 0.9]]
        left = [[x, y, h], [x, y + 1, h], [x, y + 1, h + 0.9], [x, y, h + 0.9]]
        c = ramp(z / 22)
        p.polygon(left, c, "white", 0.3)
        p.polygon(front, c, "white", 0.3)
        p.polygon(top, hexcolor([min(255, int(c[i:i + 2], 16) + 40) for i in (1, 3, 5)]), "white", 0.3)
    fig.add(_text(685, 372, f"R-pentomino, 23 generations = 23 floors, {len(vox)} voxels", 12, INK))
    fig.save("sim-life.svg")


def fig_boids():
    cases = [
        ("no rules", dict(w_sep=0, w_ali=0, w_coh=0)),
        ("alignment only", dict(w_sep=0, w_ali=1.0, w_coh=0, radius=12.0)),
        ("separation + alignment + cohesion", dict(radius=12.0)),
    ]
    fig = Figure(900, 360)
    for i, (title, params) in enumerate(cases):
        pos, vel = boids.init(150, seed=1)
        trail, v = boids.run(pos, vel, 150, **params)
        p = Panel(fig, i * 300, 0, 300, 340, [[0, 0, 0], [100, 100, 0]], title=title, pad=16)
        p.polygon([[0, 0, 0], [100, 0, 0], [100, 100, 0], [0, 100, 0]], "white", GREY, 1)
        tail = trail[-25:]
        for b in range(len(pos)):
            for k in range(len(tail) - 1):
                a, c = tail[k][b], tail[k + 1][b]
                if np.linalg.norm(a - c) < 10:             # do not draw the wrap-around jump
                    p.line([a[0], a[1], 0], [c[0], c[1], 0], ramp(k / len(tail)), 1.2, opacity=0.25 + 0.75 * k / len(tail))
        fig.add(_text(i * 300 + 150, 352, f"polarization {boids.polarization(vel):.2f} → {boids.polarization(v):.2f}", 13, INK, weight="bold"))
    fig.save("sim-boids.svg")


def fig_dla():
    cells = dla.grow(1500, seed=3)
    d = dla.fractal_dimension(cells)
    pts = [[x, y, 0] for x, y in cells]
    fig = Figure(900, 400)
    p = Panel(fig, 0, 0, 520, 400, pts, title="DLA: 1500 random walkers, each stuck where it first touched", pad=20)
    for k, (x, y) in enumerate(cells):
        square(p, x - 0.5, y - 0.5, 1, ramp(k / len(cells)), "none")
    lines = [
        ("colour = arrival order", INK, "bold"),
        ("blue: the first, orange: the last", INK, "normal"),
        ("", INK, "normal"),
        ("the tips grow, the fjords starve:", INK, "normal"),
        ("a walker from outside meets a tip", INK, "normal"),
        ("long before it finds a way in", INK, "normal"),
        ("", INK, "normal"),
        (f"fractal dimension {d:.2f}", BLUE, "bold"),
        ("(a line is 1, a filled disc is 2)", INK, "normal"),
    ]
    for i, (s, c, w) in enumerate(lines):
        fig.add(_text(560, 90 + i * 24, s, 14, c, "start", w))
    fig.save("sim-dla.svg")


if __name__ == "__main__":
    fig_life()
    fig_boids()
    fig_dla()
