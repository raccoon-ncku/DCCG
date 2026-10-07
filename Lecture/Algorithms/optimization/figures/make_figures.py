"""
Draw the figures in the Optimization README -- by running the optimizers.

    uv run Lecture/Algorithms/optimization/figures/make_figures.py

SVG helpers copied from Lecture/Lecture_05/figures/make_figures.py.
"""

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "tutorials"))
import search  # noqa: E402

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


CYCLE = [BLUE, ORANGE, GREEN, PURPLE, RED, "#f59f00", "#0ca678", "#d6336c", "#495057", "#74c0fc", "#ffa94d", "#8ce99a"]


def chart(fig, x0, y0, w, h, series, xlabel, ylabel, title, logy=False):
    """A minimal line chart. series: [(label, colour, [(x, y), ...], dashed)]."""
    xs = [x for _, _, pts, _ in series for x, _ in pts]
    ys = [y for _, _, pts, _ in series for _, y in pts]
    f = (lambda v: math.log10(v)) if logy else (lambda v: v)
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(map(f, ys)), max(map(f, ys))
    pad = (ymax - ymin) * 0.08 or 1
    ymin, ymax = ymin - pad, ymax + pad
    fig.add(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="white" stroke="{GREY}"/>')
    fig.add(_text(x0 + w / 2, y0 - 12, title, 14, INK, weight="bold"))
    fig.add(_text(x0 + w / 2, y0 + h + 30, xlabel, 11, INK))
    fig.add(_text(x0 - 8, y0 - 4, ylabel, 11, INK, "end"))
    def P(x, y):
        return (x0 + 10 + (w - 20) * (x - xmin) / (xmax - xmin or 1),
                y0 + h - 10 - (h - 20) * (f(y) - ymin) / (ymax - ymin or 1))
    for k in range(5):
        yv = ymin + (ymax - ymin) * k / 4
        _, yy = P(xmin, 10 ** yv if logy else yv)
        fig.add(_text(x0 - 4, yy + 4, f"{(10 ** yv if logy else yv):.3g}", 10, GREY, "end"))
    for k in range(5):
        xv = xmin + (xmax - xmin) * k / 4
        xx, _ = P(xv, 10 ** ymin if logy else ymin)
        fig.add(_text(xx, y0 + h + 14, f"{xv:.0f}" if xmax - xmin >= 8 else f"{xv:.3g}", 10, GREY))
    for i, (label, colour, pts, dashed) in enumerate(series):
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in (P(x, y) for x, y in pts))
        dash = ' stroke-dasharray="6,4"' if dashed else ""
        fig.add(f'<polyline points="{d}" fill="none" stroke="{colour}" stroke-width="2.5"{dash}/>')
        fig.add(_text(x0 + w - 10, y0 + 18 + i * 16, label, 11, colour, "end", "bold"))

def fig_columns():
    budget, seed = 3000, 5
    fig = Figure(900, 420)
    plan = [[x, y, 0] for x, y in search.PLAN]
    for i, (name, fn) in enumerate(search.METHODS.items()):
        layout, value, _ = fn(k=6, budget=budget, seed=seed)
        p = Panel(fig, i * 225, 0, 225, 400, plan, title=name, pad=14)
        cols = np.array(layout)
        d = np.linalg.norm(search.SAMPLES[:, None, :] - cols[None, :, :], axis=2).min(axis=1)
        s = 0.25
        for (x, y), dv in zip(search.SAMPLES, d):
            c = ramp(dv / 6.5)
            p.polygon([[x - s, y - s, 0], [x + s, y - s, 0], [x + s, y + s, 0], [x - s, y + s, 0]], c, c, 0.3)
        p.polygon(plan, "none", INK, 2)
        worst = search.SAMPLES[d.argmax()]
        for c in layout:
            p.key([c[0], c[1], 0], "", "white", 6, 1)
            p.dot([c[0], c[1], 0], 4, INK, "white")
        p.dot([worst[0], worst[1], 0], 5, RED, "white")
        fig.add(_text(i * 225 + 112, 392, f"worst point {value:.2f} m from a column", 12, INK, weight="bold"))
    fig.add(_text(450, 412, f"one seed, {budget} evaluations each; colour = distance to the nearest column; red dot = the worst point", 11, INK))
    fig.save("opt-columns.svg")


def fig_convergence():
    seeds, budget = range(8), 3000
    series, finals = [], {}
    colours = {"random search": GREY, "hill climbing": ORANGE, "simulated annealing": BLUE, "genetic algorithm": GREEN}
    for name, fn in search.METHODS.items():
        runs = []
        for s in seeds:
            _, val, hist = fn(k=6, budget=budget, seed=s)
            if name == "genetic algorithm":         # one history entry per generation of 28 evaluations
                hist = list(np.repeat(hist, 28))[:budget]
            hist = (hist + [hist[-1]] * budget)[:budget]
            runs.append(hist)
            finals.setdefault(name, []).append(val)
        mean = np.mean(runs, axis=0)
        pts = [(x, float(mean[x - 1])) for x in range(20, budget + 1, 20)]
        series.append((name, colours[name], pts, False))
    fig = Figure(900, 380)
    chart(fig, 80, 50, 470, 270, series, "objective evaluations", "m", "best so far, mean of 8 seeds")
    x0 = 610
    fig.add(_text(x0, 60, "final value, 8 seeds (m)", 14, INK, "start", "bold"))
    lo, hi = 4.4, 6.3
    for i, (name, vals) in enumerate(finals.items()):
        y = 100 + i * 60
        fig.add(_text(x0, y - 8, f"{name}: mean {np.mean(vals):.2f}", 12, colours[name], "start", "bold"))
        fig.add(f'<line x1="{x0}" y1="{y + 6}" x2="{x0 + 260}" y2="{y + 6}" stroke="{LIGHT}" stroke-width="2"/>')
        for v in vals:
            xx = x0 + 260 * (v - lo) / (hi - lo)
            fig.add(f'<circle cx="{xx:.1f}" cy="{y + 6}" r="5" fill="{colours[name]}" fill-opacity="0.6"/>')
    fig.add(_text(x0, 360, f"{lo} m (better) ←                        → {hi} m", 11, INK, "start"))
    fig.save("opt-convergence.svg")


if __name__ == "__main__":
    fig_columns()
    fig_convergence()
