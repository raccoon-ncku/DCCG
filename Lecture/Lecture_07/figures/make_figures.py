"""
Draw every figure in the Week 07 README, from the classes in class_examples/.

    uv run Lecture/Lecture_07/figures/make_figures.py

Each example is run and its objects are drawn, so the values printed on a
figure are the ones the example computes. The SVG helpers are a copy of the
ones in Lecture/Lecture_06/figures/make_figures.py, on purpose: each lecture
folder stays runnable on its own.
"""

import contextlib
import io
import math
import runpy
from pathlib import Path

HERE = Path(__file__).parent
EXAMPLES = HERE.parent / "class_examples"

INK = "#212529"
GREY = "#adb5bd"
LIGHT = "#f1f3f5"
FACE = "#e7f5ff"
BLUE = "#1c7ed6"
ORANGE = "#e8590c"
GREEN = "#2f9e44"
RED = "#e03131"
PURPLE = "#7048e8"
TIMBER = "#e8d5b5"


def example(name):
    """Run an example quietly and return its variables."""
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(str(EXAMPLES / f"{name}.py"), run_name="figures")


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

    def rect(self, x, y, w, h, fill="white", stroke=INK, width=1.5, rx=5):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{width}"/>')

    def line(self, a, b, color=INK, width=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" '
                 f'stroke-width="{width}" stroke-linecap="round"{d}/>')

    def arrow(self, a, b, color=INK, width=1.5, head=8, dash=None):
        self.line(a, b, color, width, dash)
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        self.poly([b, (b[0] - head * math.cos(ang - 0.45), b[1] - head * math.sin(ang - 0.45)),
                   (b[0] - head * math.cos(ang + 0.45), b[1] - head * math.sin(ang + 0.45))], color, color)

    def poly(self, pts, fill=TIMBER, stroke=INK, width=1.5):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"/>')

    def circle(self, x, y, r, fill=INK, stroke="white"):
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

    def card(self, x, y, w, title, rows, color=INK, fill="white", title_size=13, row_h=19):
        """A box with a heading and lines of code. Returns its height."""
        h = 30 + row_h * len(rows) + 6
        self.rect(x, y, w, h, fill, color)
        self.text(x + 10, y + 20, title, title_size, color, weight="bold", mono=True)
        self.line((x, y + 29), (x + w, y + 29), color, 1)
        for i, row in enumerate(rows):
            text, tone = row if isinstance(row, tuple) else (row, INK)
            self.text(x + 10, y + 47 + row_h * i, text, 12, tone, mono=True)
        return h


def fig_dict_vs_object():
    ns = example("01_beam_as_dict")
    post = ns["post"]
    fig = Figure(900, 300)
    fig.text(225, 24, "a dictionary, and functions somewhere else", 15, anchor="middle", weight="bold")
    fig.card(30, 45, 230, "post  (a dict)", [
        f'"start":  {post["start"]}', f'"end":    {post["end"]}', f'"width":  {post["width"]}',
        f'"height": {post["height"]}', (f'"length": {post["length"]}   stale!', RED)], BLUE, FACE)
    for i, name in enumerate(("volume(beam)", "cut_list(beams)", "to_boxes(beam)", "check(beam)")):
        y = 60 + i * 52
        fig.rect(310, y, 130, 32, LIGHT, GREY)
        fig.text(375, y + 21, name, 12, anchor="middle", mono=True)
        fig.line((310, y + 16), (262, 110 + i * 6), GREY, 1.2, "4 3")
    fig.text(225, 280, "which functions go with this? which keys must it have?", 12, "#495057", "middle")

    b = example("02_beam_as_class")["post"]
    fig.text(675, 24, "an object: the data and what it can do", 15, anchor="middle", weight="bold")
    fig.card(520, 45, 310, "post  (a Beam)", [
        f"name   = {b.name!r}", f"start  = {b.start}", f"end    = {b.end}", f"width  = {b.width}", f"height = {b.height}",
        ("length()    computed when asked", GREEN), ("volume()    uses its own values", GREEN),
        ("__repr__()  says what it is", GREEN)], GREEN, "#ebfbee")
    fig.text(675, 280, "one definition says what a beam has and what it can do", 12, "#495057", "middle")
    fig.save("class-dict-vs-object.svg")


def fig_class_and_objects():
    ns = example("02_beam_as_class")
    post, plate = ns["post"], ns["plate"]
    fig = Figure(900, 370)
    fig.text(120, 24, "one class", 15, anchor="middle", weight="bold")
    fig.card(20, 45, 200, "class Beam", ["__init__(self, ...)", "length(self)", "volume(self)"], PURPLE, "#f3f0ff")
    fig.text(120, 170, "the definition: it holds", 12, "#495057", "middle")
    fig.text(120, 186, "no beam, and no numbers", 12, "#495057", "middle")

    fig.text(420, 24, "as many objects as you make", 15, anchor="middle", weight="bold")
    h = fig.card(310, 45, 220, "post", [f"start = {post.start}", f"end   = {post.end}", f"width = {post.width}",
                                        (f"post.length() -> {post.length():.0f}", BLUE)], BLUE, FACE)
    fig.card(310, 45 + h + 24, 220, "plate", [f"start = {plate.start}", f"end   = {plate.end}", f"width = {plate.width}",
                                              (f"plate.length() -> {plate.length():.0f}", ORANGE)], ORANGE, "#fff4e6")
    fig.arrow((222, 85), (308, 85), PURPLE)
    fig.arrow((222, 95), (308, 45 + h + 50), PURPLE)
    fig.text(265, 77, "Beam(...)", 11, PURPLE, "middle", mono=True)

    # the same two objects, drawn to scale from their own values
    x0, y0, s = 600, 310, 0.075
    fig.text(735, 24, "the two beams, to scale", 15, anchor="middle", weight="bold")
    pw = post.width * s
    fig.rect(x0 - pw / 2, y0 - post.length() * s, pw, post.length() * s, "#a5d8ff", BLUE, 1.5, 1)
    fig.rect(x0 - 50 * s, y0 - post.length() * s - 50 * s, plate.length() * s + 50 * s, plate.width * s, "#ffd8a8", ORANGE, 1.5, 1)
    fig.text(x0 - 10, y0 - 90, "post", 13, BLUE, "end", "bold")
    fig.text(x0 + 130, y0 - post.length() * s - 12, "plate", 13, ORANGE, "middle", "bold")

    fig.line((20, 345), (880, 345), LIGHT, 1)
    fig.text(20, 362, "post.length()", 13, BLUE, weight="bold", mono=True)
    fig.text(135, 362, "is the same call as", 12, "#495057")
    fig.text(250, 362, "Beam.length(post)", 13, PURPLE, weight="bold", mono=True)
    fig.text(395, 362, ": inside the method, self is the object before the dot.", 12, "#495057")
    fig.save("class-and-objects.svg")


def fig_derive():
    ns = example("04_derive_dont_store")
    stale, fresh = ns["stale"], ns["fresh"]
    fig = Figure(760, 330)

    def panel(x, title, code, value, tone):
        s, base = 0.07, 300
        fig.text(x + 170, 24, title, 15, anchor="middle", weight="bold")
        fig.text(x + 170, 44, code, 12, "#495057", "middle", mono=True)
        real = fresh.end[2]
        fig.rect(x + 80, base - real * s, 16, real * s, TIMBER, INK, 1.5, 1)
        fig.line((x + 70, base - 2400 * s), (x + 106, base - 2400 * s), GREY, 1.2, "4 3")
        fig.text(x + 112, base - 2400 * s + 4, "the old end", 11, "#868e96")
        fig.text(x + 112, base - real * s + 4, f"end moved to z = {real}", 12)
        fig.text(x + 170, base - 40, ".length", 13, INK, weight="bold", mono=True)
        fig.text(x + 170, base - 14, str(value), 22, tone, weight="bold")

    panel(20, "stored in __init__", "self.length = math.dist(...)", stale.length, RED)
    panel(400, "derived with @property", "return math.dist(...)", fresh.length, GREEN)
    fig.save("class-derive.svg")


def fig_references():
    ns = example("06_objects_hold_objects")
    fig = Figure(860, 250)
    fig.text(220, 24, "a name is a label, not a copy", 15, anchor="middle", weight="bold")
    for i, (name, code) in enumerate((("post", 'Beam("post", ...)'), ("same", "post"), ("twin", "copy.copy(post)"))):
        y = 58 + i * 58
        fig.text(20, y + 5, f"{name} = {code}", 12, mono=True)
    fig.card(270, 40, 170, "a Beam", ["end = (0, 0, 3000)", ("length -> 3000", BLUE)], BLUE, FACE)
    fig.card(270, 140, 170, "another Beam", ["end = (0, 0, 2400)", ("length -> 2400", ORANGE)], ORANGE, "#fff4e6")
    fig.arrow((200, 56), (268, 70), BLUE)
    fig.arrow((108, 112), (268, 90), BLUE)
    fig.arrow((186, 171), (268, 180), ORANGE)

    joint = ns["frame"].joints[1]
    fig.text(660, 24, "a joint holds the beams themselves", 15, anchor="middle", weight="bold")
    fig.card(500, 95, 110, f"Joint", ["a", "b"], PURPLE, "#f3f0ff")
    fig.card(690, 45, 150, f"Beam {joint.a.name!r}", [f"length -> {joint.a.length:.0f}"], BLUE, FACE)
    fig.card(690, 150, 150, f"Beam {joint.b.name!r}", [f"length -> {joint.b.length:.0f}"], ORANGE, "#fff4e6")
    fig.arrow((612, 142), (688, 80), BLUE)
    fig.arrow((612, 161), (688, 185), ORANGE)
    fig.text(660, 240, "move the post and the joint sees it: nothing to update", 12, "#495057", "middle")
    fig.save("class-references.svg")


def fig_objects_are_a_graph():
    ns = example("06_objects_hold_objects")
    frame = ns["frame"]
    fig = Figure(900, 310)
    s, x0, y0 = 0.052, 40, 255
    to_page = lambda p: (x0 + p[0] * s, y0 - p[2] * s)

    fig.text(130, 24, "a frame", 15, anchor="middle", weight="bold")
    colours = {"sill": ORANGE, "post": BLUE, "cap": GREEN}
    for beam in frame.beams:
        fig.line(to_page(beam.start), to_page(beam.end), colours[beam.name], 9)
        mx, my = to_page(tuple((a + b) / 2 for a, b in zip(beam.start, beam.end)))
        fig.text(mx + (14 if beam.name == "post" else 0), my + (20 if beam.name != "post" else 4), beam.name, 13,
                 colours[beam.name], "start" if beam.name == "post" else "middle", "bold")

    fig.text(470, 24, "the objects that describe it", 15, anchor="middle", weight="bold")
    fig.card(290, 110, 100, "Frame", ["beams", "joints"], PURPLE, "#f3f0ff")
    fig.card(420, 55, 110, "Joint", ["a", "b"], "#495057", LIGHT)
    fig.card(420, 180, 110, "Joint", ["a", "b"], "#495057", LIGHT)
    ys = {"sill": 45, "post": 125, "cap": 205}
    for name, y in ys.items():
        fig.rect(570, y, 86, 34, "white", colours[name])
        fig.text(613, y + 22, name, 12, colours[name], "middle", "bold", mono=True)
    fig.arrow((392, 170), (418, 90), "#495057")
    fig.arrow((392, 175), (418, 205), "#495057")
    fig.arrow((532, 92), (568, 137), BLUE, 1.3)
    fig.arrow((532, 110), (568, 65), ORANGE, 1.3)
    fig.arrow((532, 217), (568, 145), BLUE, 1.3)
    fig.arrow((532, 235), (568, 225), GREEN, 1.3)

    fig.text(790, 24, "the same thing, as a graph", 15, anchor="middle", weight="bold")
    pos = {"sill": (725, 225), "post": (790, 95), "cap": (855, 225)}
    fig.line(pos["post"], pos["sill"], INK, 2)
    fig.line(pos["post"], pos["cap"], INK, 2)
    for name, (x, y) in pos.items():
        fig.circle(x, y, 13, colours[name])
        fig.text(x, y - 18, name, 12, colours[name], "middle", "bold")
    fig.text(450, 300, "objects that hold references to objects are a graph. compas_timber keeps that graph explicitly, in model.graph.",
             13, INK, "middle")
    fig.save("class-objects-are-a-graph.svg")


def fig_inheritance():
    ns = example("07_inheritance")
    Beam, Butt, Miter = ns["Beam"], ns["ButtJoint"], ns["MiterJoint"]
    post, plate = Beam("post", 2400, 100), Beam("plate", 3600, 100)
    fig = Figure(860, 430)
    fig.card(290, 15, 280, "class Joint", ["blank(beam)", ("allowance(beam)  # each child answers", RED)], PURPLE, "#f3f0ff")
    fig.line((430, 89), (430, 118), PURPLE)
    fig.line((215, 118), (645, 118), PURPLE)

    def corner(x, cls, tone, fill, formula):
        fig.line((x + 195, 118), (x + 195, 130), PURPLE)
        fig.card(x + 40, 130, 310, f"class {cls.__name__}(Joint)", [formula], tone, fill)
        joint = cls(post, plate)
        # a corner to scale, looking along the third axis: the post rises to the plate's centreline
        s, cx, cy = 0.5, x + 70, 250
        half = 50
        reach = 300
        down = cy + 120
        if cls is Butt:
            fig.poly([(cx - half * s, down), (cx - half * s, cy + half * s), (cx + half * s, cy + half * s), (cx + half * s, down)], "#a5d8ff", BLUE)
            fig.poly([(cx - half * s, cy - half * s), (cx + reach, cy - half * s), (cx + reach, cy + half * s), (cx - half * s, cy + half * s)], "#ffd8a8", ORANGE)
        else:
            fig.poly([(cx - half * s, down), (cx - half * s, cy - half * s), (cx + half * s, cy + half * s), (cx + half * s, down)], "#a5d8ff", BLUE)
            fig.poly([(cx - half * s, cy - half * s), (cx + reach, cy - half * s), (cx + reach, cy + half * s), (cx + half * s, cy + half * s)], "#ffd8a8", ORANGE)
        fig.line((cx, cy), (cx, down + 8), INK, 1, "6 3")
        fig.line((cx, cy), (cx + reach + 8, cy), INK, 1, "6 3")
        fig.text(cx + half * s + 6, down - 6, "post", 12, BLUE, weight="bold")
        fig.text(cx + reach - 36, cy - half * s - 8, "plate", 12, ORANGE, weight="bold")
        fig.text(cx + 45, 325, f"joint.blank(post)  -> {joint.blank(post):.0f}", 12, BLUE, mono=True)
        fig.text(cx + 45, 345, f"joint.blank(plate) -> {joint.blank(plate):.0f}", 12, ORANGE, mono=True)

    corner(20, Butt, BLUE, FACE, "post stops, plate runs on")
    corner(450, Miter, ORANGE, "#fff4e6", "both reach the outer corner")
    fig.text(430, 415, "the same call on either object. the dashed lines are the centrelines, 2400 and 3600 long.", 13, INK, "middle")
    fig.save("class-inheritance.svg")


def fig_component():
    ns = example("09_a_component_is_a_class")
    inputs, outputs = ns["METADATA"]["inputs"], ns["METADATA"]["outputs"]
    fig = Figure(900, 400)

    # a component as Grasshopper draws it, with the names from metadata.json
    x, y, w, h = 120, 40, 150, 110
    fig.text(195, 24, "on the canvas", 15, anchor="middle", weight="bold")
    fig.rect(x, y, w, h, "#ced4da", INK, 2, 8)
    fig.text(x + w / 2, y + h / 2 + 5, "Stud Wall", 14, INK, "middle", "bold")
    for i, name in enumerate(inputs):
        py = y + (i + 1) * h / (len(inputs) + 1)
        fig.circle(x, py, 5, "white", INK)
        fig.text(x - 10, py + 4, name, 12, BLUE, "end", "bold", mono=True)
    for i, name in enumerate(outputs):
        py = y + (i + 1) * h / (len(outputs) + 1)
        fig.circle(x + w, py, 5, "white", INK)
        fig.text(x + w + 10, py + 4, name, 12, GREEN, "start", "bold", mono=True)

    fig.text(650, 24, "in code.py", 15, anchor="middle", weight="bold")
    fig.card(430, 40, 440, "class Cs_StudWall(component):", [
        ("    def RunScript(self, length, height, spacing):", BLUE),
        "        wall = StudWall(length, height, spacing)",
        "        lines = [line_to_rhino(l) for l in ...]",
        ("        return lines, wall.n_studs", GREEN)], PURPLE, "#f8f9fa")
    fig.text(650, 170, "the names on the ports are the names of the parameters", 12, "#495057", "middle")
    fig.text(650, 186, "metadata.json lists them too: the two must agree", 12, "#495057", "middle")

    # who calls whom
    steps = [("you move a slider", LIGHT, INK), ("Grasshopper calls\nRunScript", "#f3f0ff", PURPLE),
             ("the adapter calls\nthe core", "#f3f0ff", PURPLE), ("StudWall computes\nCOMPAS lines", "#ebfbee", GREEN),
             ("the adapter converts\nto Rhino lines", "#f3f0ff", PURPLE), ("values appear on\nthe output ports", LIGHT, INK)]
    fig.text(450, 222, "who calls whom", 15, anchor="middle", weight="bold")
    bw, gap, top = 130, 18, 240
    for i, (label, fill, tone) in enumerate(steps):
        bx = 22 + i * (bw + gap)
        fig.rect(bx, top, bw, 60, fill, tone)
        for j, part in enumerate(label.split("\n")):
            fig.text(bx + bw / 2, top + 26 + j * 16, part, 12, tone, "middle")
        if i < len(steps) - 1:
            fig.arrow((bx + bw + 1, top + 30), (bx + bw + gap - 1, top + 30), INK)
    fig.text(450, 330, "you never write Cs_StudWall() or call RunScript yourself: the framework calls you.", 13, INK, "middle", "bold")
    fig.rect(22, 345, 856, 44, "#ebfbee", GREEN)
    fig.text(450, 364, "only the green box has logic, and it is the only part pytest can reach. it knows nothing of Grasshopper.", 12, INK, "middle")
    fig.text(450, 381, "the adapter is a component (inheritance) and has a StudWall (composition).", 12, INK, "middle")
    fig.save("class-component.svg")


if __name__ == "__main__":
    fig_dict_vs_object()
    fig_class_and_objects()
    fig_derive()
    fig_references()
    fig_objects_are_a_graph()
    fig_inheritance()
    fig_component()
