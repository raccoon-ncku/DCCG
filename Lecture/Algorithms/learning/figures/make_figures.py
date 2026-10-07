"""
Draw the figures in the Learning README -- by running the tutorials.

    uv run Lecture/Algorithms/learning/figures/make_figures.py

SVG helpers copied from Lecture/Lecture_05/figures/make_figures.py.
"""

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "tutorials"))
import kmeans as km  # noqa: E402
import regression as rg  # noqa: E402

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

def fig_panels():
    X = km.roof_panels()
    k, (labels, centres, _, _) = km.families_needed(X, tolerance=10.0)
    n = 14
    fig = Figure(900, 400)
    # left: the roof plan, each panel coloured by family
    p = Panel(fig, 0, 0, 400, 380, [[0, 0, 0], [14, 14, 0]], title=f"196 roof panels → {k} families (±10 mm)", pad=22)
    for idx in range(n * n):
        i, j = divmod(idx, n)
        c = CYCLE[labels[idx] % len(CYCLE)]
        p.polygon([[i, j, 0], [i + 1, j, 0], [i + 1, j + 1, 0], [i, j + 1, 0]], c, "white", 1.5)
    fig.add(_text(200, 372, "a 14 × 14 m spherical-cap roof (R = 25 m), plan view", 11, INK))
    # right: feature space
    p = Panel(fig, 420, 0, 480, 380, [[1000, 1000, 0], [1040, 1040, 0]], title="each panel as a point: width × depth (mm)", pad=40)
    for (w, d), l in zip(X, labels):
        cw, cd = centres[l]
        p.line([w, d, 0], [cw, cd, 0], CYCLE[l % len(CYCLE)], 1, opacity=0.5)
        p.dot([w, d, 0], 4, CYCLE[l % len(CYCLE)])
    for j, (w, d) in enumerate(centres):
        p.dot([w, d, 0], 7, "white", CYCLE[j % len(CYCLE)])
    fig.add(_text(660, 372, f"rings: family templates (the cluster centres) · {len(np.unique(X.round(1), axis=0))} distinct sizes → {k}", 11, INK))
    fig.save("learn-panels.svg")


def fig_regression():
    L, h, d = rg.beam_experiments(n=60)
    c, a, e = rg.fit_power_law(L, h, d)
    fig = Figure(900, 400)
    # left: measured vs predicted, log-log
    pred = np.exp(c + a * np.log(L) + e * np.log(h))
    lo, hi = math.log10(min(d.min(), pred.min())), math.log10(max(d.max(), pred.max()))
    p = Panel(fig, 0, 0, 430, 360, [[lo, lo, 0], [hi, hi, 0]], title="60 noisy 'simulations' vs the fitted law", pad=40)
    p.line([lo, lo, 0], [hi, hi, 0], GREY, 1.5, dash="5,4")
    for m, q in zip(d, pred):
        p.dot([math.log10(q), math.log10(m), 0], 4, BLUE)
    fig.add(_text(215, 330, "predicted deflection (log)  →", 11, INK))
    fig.add(_text(215, 352, f"fitted: deflection ∝ L^{a:.2f} · h^{e:.2f}", 14, BLUE, weight="bold"))
    fig.add(_text(215, 372, "true law: L^4 · h^-3 (Euler–Bernoulli), never shown to the fit", 12, INK))
    # right: overfitting
    x, y = rg.daylight_samples()
    train, test = rg.split(len(x), seed=4)
    degrees = list(range(1, 13))
    errs = rg.polynomial_errors(x, y, degrees, train, test)
    chart(fig, 520, 50, 340, 270,
          [("train error", ORANGE, [(dd, errs[dd][0]) for dd in degrees], False),
           ("test error", BLUE, [(dd, errs[dd][1]) for dd in degrees], False)],
          "polynomial degree", "RMSE", "more flexible ≠ better", logy=True)
    fig.add(_text(690, 390, "training error keeps falling; test error climbs once the curve fits noise", 12, INK))
    fig.save("learn-regression.svg")


if __name__ == "__main__":
    fig_panels()
    fig_regression()
