# ──────────────────────────────────────────────────────────────────────────────
#  READ ONLY  ·  this file is the SPEC, not the answers.
#
#  If a checkpoint fails, edit `../tasks.py` (or `../core.py` / `../runner.py`
#  in Week 06), NOT this file. Read the assertions below to understand what
#  each checkpoint is checking; do not change them.
# ──────────────────────────────────────────────────────────────────────────────
"""
The SPECIFICATION for Week 06.

Two kinds of test live here, and the difference matters.

Most tests RUN your code and check what it returns. `test_core_is_pure` does
something else: it READS your core.py as text, parses it, and inspects the
import statements. That is a *structural* test -- it checks a property of the
code itself rather than of its behaviour.

Structural tests are how architecture rules survive contact with a deadline.
A rule nothing enforces is a rule that quietly stops being true.
"""

import ast
from pathlib import Path

import compas
import compas.geometry as cg
import pytest

import core
from runner import build_artifact

HERE = Path(__file__).parent
TOL = 1e-9


def approx(a, b, tol=TOL):
    return abs(a - b) < tol


# --- 1. the core builds a wall ----------------------------------------------

def test_wall_has_one_box_per_course():
    """stacked_wall() returns exactly n_courses boxes"""
    assert len(core.stacked_wall(5)) == 5
    assert len(core.stacked_wall(1)) == 1


def test_wall_sits_on_the_ground():
    """the bottom of the lowest course is at z = 0"""
    boxes = core.stacked_wall(4, course_height=0.25)
    lowest = min(c.z for box in boxes for c in box.points)
    assert approx(lowest, 0.0), f"The wall starts at z={lowest}, not 0."


def test_wall_courses_are_stacked_without_gaps_or_overlaps():
    """each course starts exactly where the one below it ended"""
    # A property test: we do not care about absolute positions, only that the
    # relationship between neighbours holds. This one assertion rules out
    # floating courses, overlapping courses, and wrong spacing at once.
    height = 0.25
    boxes = core.stacked_wall(6, course_height=height)
    for i, box in enumerate(boxes):
        bottom = min(c.z for c in box.points)
        top = max(c.z for c in box.points)
        assert approx(bottom, i * height), (
            f"course {i} starts at z={bottom}, expected {i * height}"
        )
        assert approx(top, (i + 1) * height), (
            f"course {i} ends at z={top}, expected {(i + 1) * height}"
        )


def test_wall_is_returned_bottom_course_first():
    """boxes come back in order, lowest first"""
    boxes = core.stacked_wall(4)
    heights = [box.frame.point.z for box in boxes]
    assert heights == sorted(heights), "Courses are not ordered bottom to top."


def test_odd_courses_are_offset_and_even_ones_are_not():
    """odd courses are shifted along X; even courses are centred on x = 0"""
    boxes = core.stacked_wall(4, offset=0.1)
    assert approx(boxes[0].frame.point.x, 0.0), "course 0 is even: no offset"
    assert approx(boxes[1].frame.point.x, 0.1), "course 1 is odd: offset by 0.1"
    assert approx(boxes[2].frame.point.x, 0.0), "course 2 is even: no offset"
    assert approx(boxes[3].frame.point.x, 0.1), "course 3 is odd: offset by 0.1"


def test_wall_dimensions_follow_the_parameters():
    """length and thickness are respected, not hard-coded"""
    boxes = core.stacked_wall(2, length=3.5, thickness=0.44, course_height=0.11)
    for box in boxes:
        assert approx(box.xsize, 3.5)
        assert approx(box.ysize, 0.44)
        assert approx(box.zsize, 0.11)


def test_wall_rejects_nonsense_input():
    """stacked_wall(0) raises ValueError rather than returning []"""
    # A wall with no courses is not a wall -- it is a caller who has made a
    # mistake and would rather find out here than three functions later.
    with pytest.raises(ValueError):
        core.stacked_wall(0)
    with pytest.raises(ValueError):
        core.stacked_wall(-3)


# --- 2. the derived value ---------------------------------------------------

def test_wall_height_matches_the_geometry():
    """wall_height() agrees with the wall the core actually builds"""
    # The interesting part: this checks a COMPUTED number against a MEASURED
    # one. If they ever disagree, one of the two is lying.
    for n in (1, 5, 12):
        boxes = core.stacked_wall(n, course_height=0.3)
        measured = max(c.z for box in boxes for c in box.points)
        assert approx(core.wall_height(n, 0.3), measured)


def test_wall_height_rejects_nonsense_input():
    """wall_height(0) raises ValueError too"""
    with pytest.raises(ValueError):
        core.wall_height(0)


# --- 3. the architecture rule, enforced -------------------------------------

FORBIDDEN_IMPORTS = {
    "compas_viewer": "a viewer is presentation, not geometry",
    "json": "file formats belong in the runner",
    "pathlib": "paths belong in the runner",
    "os": "the filesystem belongs in the runner",
    "sys": "the runtime environment belongs in the runner",
    "rhino": "the core must not know Rhino exists",
    "rhinoscriptsyntax": "the core must not know Rhino exists",
    "Rhino": "the core must not know Rhino exists",
    "scriptcontext": "the core must not know Rhino exists",
}


def _imported_module_names(path):
    """Every top-level module name imported by a Python file."""
    tree = ast.parse(path.read_text())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


def test_core_is_pure():
    """core.py imports nothing from the outside world (a structural test)"""
    imported = _imported_module_names(HERE / "core.py")
    for name in sorted(imported):
        assert name not in FORBIDDEN_IMPORTS, (
            f"core.py imports `{name}` -- {FORBIDDEN_IMPORTS[name]}.\n"
            "Move whatever needs it into runner.py. The core has to stay "
            "importable on a machine with no screen, no Rhino, and no files."
        )


def test_core_does_not_print_or_open_files():
    """core.py contains no print() or open() calls"""
    tree = ast.parse((HERE / "core.py").read_text())
    called = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    for banned, why in (("print", "returning a value"), ("open", "the runner")):
        assert banned not in called, (
            f"core.py calls {banned}(). A pure function communicates by "
            f"{why}, not by reaching out of itself."
        )


def test_runner_does_not_reimplement_the_geometry():
    """runner.py calls the core rather than building boxes itself"""
    tree = ast.parse((HERE / "runner.py").read_text())
    used = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    attrs = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)}
    assert "Box" not in used and "Frame" not in used, (
        "runner.py builds geometry directly. Geometry logic lives in core.py; "
        "the runner's job is to call it and save the result."
    )
    assert "stacked_wall" in (used | attrs), (
        "runner.py never calls core.stacked_wall(). The runner is supposed to "
        "be a thin layer over the core, not a parallel implementation."
    )


# --- 4. the artifact --------------------------------------------------------

def test_build_artifact_writes_a_file(tmp_path):
    """build_artifact() creates the file it was asked for"""
    path = tmp_path / "out" / "wall.json"
    build_artifact(path, n_courses=6)
    assert path.exists(), (
        "No file was written. Did you create the parent folder? "
        "mkdir(parents=True, exist_ok=True)."
    )


def test_build_artifact_returns_the_geometry(tmp_path):
    """build_artifact() also returns the boxes it built"""
    boxes = build_artifact(tmp_path / "wall.json", n_courses=6)
    assert len(boxes) == 6
    assert all(isinstance(b, cg.Box) for b in boxes)


def test_artifact_round_trips_as_real_compas_objects(tmp_path):
    """the saved artifact loads back as Boxes, not as plain dictionaries"""
    # This is what compas.json_dump buys you over the plain json module, and
    # it is why the adapter in Week 14 can be four lines long.
    path = tmp_path / "wall.json"
    build_artifact(path, n_courses=5, course_height=0.3)
    loaded = compas.json_load(path)
    assert len(loaded) == 5
    assert all(isinstance(b, cg.Box) for b in loaded), (
        "The artifact did not come back as Box objects. Use compas.json_dump, "
        "not json.dumps."
    )
    assert approx(max(c.z for b in loaded for c in b.points), 1.5)


def test_artifact_passes_parameters_through(tmp_path):
    """extra keyword arguments reach the core"""
    boxes = build_artifact(tmp_path / "wall.json", n_courses=3, length=4.0)
    assert all(approx(b.xsize, 4.0) for b in boxes), (
        "length=4.0 never reached the core. Forward **kwargs through."
    )
