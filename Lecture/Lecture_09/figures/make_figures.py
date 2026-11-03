"""
Draw the Part C figures of the Week 09 README.

    uv run Lecture/Lecture_09/figures/make_figures.py

The scaffold figure refuses to draw a path that the project template does not
have. The SVG helpers are copied from the other weeks, on purpose: each lecture
folder stays runnable on its own.
"""

import math
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE = HERE.parents[1] / "Lecture_12" / "project_template"

INK = "#212529"
GREY = "#868e96"
LIGHT = "#f1f3f5"
BLUE = "#1c7ed6"
ORANGE = "#e8590c"
GREEN = "#2f9e44"
RED = "#e03131"
PURPLE = "#7048e8"


class Figure:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.items = []

    def add(self, item):
        self.items.append(item)

    def save(self, name):
        body = "\n".join(self.items)
        (HERE / name).write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}" font-family="Helvetica, Arial, sans-serif">\n'
            f'<rect width="100%" height="100%" fill="white"/>\n{body}\n</svg>\n'
        )
        print("wrote", name)

    def text(self, x, y, s, size=12, color=INK, anchor="start", weight="normal", mono=False):
        s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        family = ' font-family="Menlo, Consolas, monospace"' if mono else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" text-anchor="{anchor}" '
                 f'font-weight="{weight}" xml:space="preserve"{family}>{s}</text>')

    def rect(self, x, y, w, h, fill="white", stroke=INK, width=1.5, rx=6):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{width}"/>')

    def arrow(self, a, b, color=INK, width=1.5, head=8):
        self.add(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" '
                 f'stroke-width="{width}" stroke-linecap="round"/>')
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        pts = [b, (b[0] - head * math.cos(ang - 0.45), b[1] - head * math.sin(ang - 0.45)),
               (b[0] - head * math.cos(ang + 0.45), b[1] - head * math.sin(ang + 0.45))]
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<polygon points="{d}" fill="{color}" stroke="{color}"/>')


def fig_scaffold():
    rows = [
        ("pyproject.toml", "pyproject.toml", "what this is, which Python, which libraries", GREY, "#f8f9fa"),
        ("src/my_tool/", "src/my_tool", "CORE: your classes and functions. Pure Python + COMPAS, no Rhino", GREEN, "#ebfbee"),
        ("tests/", "tests", "SPEC: what correct means. Runs anywhere, in seconds", BLUE, "#e7f5ff"),
        ("components/Mt_*/", "components/Mt_ColumnGrid", "ADAPTERS: find the core, call it, convert. No logic", PURPLE, "#f3f0ff"),
        ("scripts/ghuser", "scripts/ghuser", "BUILD: components/ to dist/, in Docker, no Rhino needed", ORANGE, "#fff4e6"),
        (".github/workflows/", ".github/workflows", "PIPELINE: the tests and the build, on every push", GREY, "#f8f9fa"),
    ]
    fig = Figure(860, 60 + 46 * len(rows))
    fig.text(20, 28, "my_tool/", 15, INK, weight="bold", mono=True)
    for i, (path, real, what, tone, fill) in enumerate(rows):
        assert (TEMPLATE / real).exists(), real
        y = 44 + i * 46
        fig.rect(20, y, 820, 38, fill, tone)
        fig.text(34, y + 24, path, 13, tone, weight="bold", mono=True)
        fig.text(230, y + 24, what, 13, INK)
    fig.save("se-scaffold.svg")


def fig_loop():
    fig = Figure(880, 340)
    fig.rect(20, 30, 190, 74, LIGHT, GREY)
    fig.text(115, 54, "the brief", 14, INK, "middle", "bold")
    fig.text(115, 74, "a sentence a person", 12, INK, "middle")
    fig.text(115, 90, "could say", 12, INK, "middle")
    fig.arrow((212, 67), (258, 67))
    fig.rect(260, 30, 240, 74, "#e7f5ff", BLUE)
    fig.text(380, 54, "the spec", 14, BLUE, "middle", "bold")
    fig.text(380, 74, "tests/test_stud_wall.py", 12, INK, "middle", mono=True)
    fig.text(380, 90, "the same sentence, checkable", 12, INK, "middle")
    fig.arrow((300, 106), (180, 148))

    boxes = [(120, "RED", RED, "#fff5f5", ["write one test, watch it fail", "E  assert 2.8 == 3.0"]),
             (380, "GREEN", GREEN, "#ebfbee", ["the least code that passes", "and no more"]),
             (640, "REFACTOR", PURPLE, "#f3f0ff", ["tidy, rename, delete", "tests stay green"])]
    for cx, name, tone, fill, lines in boxes:
        fig.rect(cx - 110, 150, 220, 88, fill, tone)
        fig.text(cx, 174, name, 14, tone, "middle", "bold")
        for j, line in enumerate(lines):
            fig.text(cx, 196 + j * 18, line, 12, INK, "middle", mono="assert" in line)
    fig.arrow((232, 194), (268, 194))
    fig.arrow((492, 194), (528, 194))
    fig.add('<path d="M 640 240 C 640 292, 120 292, 120 248" fill="none" stroke="#212529" stroke-width="1.5"/>')
    fig.arrow((120, 256), (120, 241))
    fig.text(380, 300, "next sentence of the brief", 12, GREY, "middle")
    fig.arrow((752, 194), (800, 194))
    fig.text(808, 190, "commit", 12, INK, weight="bold")
    fig.text(440, 326, "uv run pytest after every change. uv run --python 3.9 pytest before you commit.", 13, INK, "middle", mono=True)
    fig.save("se-loop.svg")


def fig_build():
    fig = Figure(900, 250)
    fig.rect(20, 30, 200, 60, "#f3f0ff", PURPLE)
    fig.text(120, 55, "components/Mt_*/", 13, PURPLE, "middle", "bold", mono=True)
    fig.text(120, 75, "code.py, metadata.json, icon", 11, INK, "middle")
    fig.rect(20, 110, 200, 60, "#ebfbee", GREEN)
    fig.text(120, 135, "src/my_tool/", 13, GREEN, "middle", "bold", mono=True)
    fig.text(120, 155, "the core", 11, INK, "middle")

    fig.rect(270, 20, 280, 160, "#fff4e6", ORANGE)
    fig.text(410, 44, "scripts/ghuser", 13, ORANGE, "middle", "bold", mono=True)
    fig.text(410, 62, "docker run ... ghuser-build", 11, INK, "middle", mono=True)
    for i, step in enumerate(("1. componentize: folder to .ghuser", "2. verify: read every file back", "3. package: components + core")):
        fig.text(288, 92 + i * 26, step, 13, INK)
    fig.arrow((222, 60), (268, 80))
    fig.arrow((222, 140), (268, 120))

    fig.rect(600, 20, 150, 74, "white", INK)
    fig.text(675, 46, "dist/ghuser/", 12, INK, "middle", "bold", mono=True)
    fig.text(675, 66, "Mt_*.ghuser", 12, INK, "middle", mono=True)
    fig.rect(600, 106, 150, 74, "white", INK)
    fig.text(675, 132, "dist/", 12, INK, "middle", "bold", mono=True)
    fig.text(675, 152, "my-tool-*.yak", 12, INK, "middle", mono=True)
    fig.arrow((552, 70), (598, 58))
    fig.arrow((552, 130), (598, 142))

    fig.rect(790, 106, 90, 74, LIGHT, GREY)
    fig.text(835, 138, "Rhino 8", 13, INK, "middle", "bold")
    fig.text(835, 156, "drag it in", 11, INK, "middle")
    fig.arrow((752, 143), (788, 143))

    fig.text(385, 214, "no Rhino and no Windows up to here: the same image runs on a laptop and in CI", 13, INK, "middle")
    fig.save("se-build.svg")


if __name__ == "__main__":
    fig_scaffold()
    fig_loop()
    fig_build()
