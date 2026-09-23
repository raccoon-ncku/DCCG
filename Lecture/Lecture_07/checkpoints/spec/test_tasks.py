# ──────────────────────────────────────────────────────────────────────────────
#  READ ONLY  ·  this file is the SPEC, not the answers.
#
#  Your work goes in  ../answers.py  (or ../answers_core.py + ../answers_runner.py
#  in Week 06). That file is auto-created from the shipped starter on first run
#  and is gitignored, so `git pull` never conflicts with it. Read the
#  assertions below to understand what each checkpoint is checking; do not
#  change them.
# ──────────────────────────────────────────────────────────────────────────────
"""
The SPECIFICATION for Week 07.

Read how a class gets specified: not "it is a vector", but a list of small,
checkable promises -- this constructor works, this operator does that, this
property stays correct after you change something.

If you cannot write that list for a class you are designing, the class is not
finished being designed.
"""

import ast
import math
from pathlib import Path

import compas.geometry as cg
import pytest

from answers import Rectangle, Square, Vector2D, Wall

HERE = Path(__file__).parent
TOL = 1e-9


def approx(a, b, tol=TOL):
    return abs(a - b) < tol


# --- 1. Vector2D ------------------------------------------------------------

def test_vector_stores_its_components():
    """Vector2D(3, 4) has .x == 3 and .y == 4"""
    v = Vector2D(3, 4)
    assert v.x == 3 and v.y == 4


def test_vector_repr_is_readable():
    """repr(Vector2D(3, 4)) is exactly 'Vector2D(3, 4)'"""
    assert repr(Vector2D(3, 4)) == "Vector2D(3, 4)"


def test_vector_addition():
    """v1 + v2 returns a new Vector2D with the components summed"""
    result = Vector2D(1, 2) + Vector2D(10, 20)
    assert isinstance(result, Vector2D)
    assert result.x == 11 and result.y == 22


def test_vector_addition_does_not_modify_the_operands():
    """a + b leaves both a and b unchanged"""
    a, b = Vector2D(1, 2), Vector2D(10, 20)
    a + b
    assert (a.x, a.y) == (1, 2) and (b.x, b.y) == (10, 20)


def test_vector_equality_compares_values():
    """two vectors with the same components are equal"""
    assert Vector2D(3, 4) == Vector2D(3, 4)
    assert not (Vector2D(3, 4) == Vector2D(4, 3))


def test_vector_length_is_a_property():
    """v.length is accessed WITHOUT parentheses"""
    v = Vector2D(3, 4)
    assert approx(v.length, 5.0), (
        "If this raised a TypeError, `length` is a method. Add @property "
        "above it -- see README section 4."
    )


def test_vector_length_stays_correct_after_a_change():
    """changing .x updates .length -- it is derived, not stored"""
    v = Vector2D(3, 4)
    v.x = 6
    assert approx(v.length, math.hypot(6, 4)), (
        "length is stale. You computed it once in __init__ and stored it. "
        "Derive it in a @property instead."
    )


def test_vector_unitized_has_length_one():
    """unitized() returns a new vector of length 1, pointing the same way"""
    v = Vector2D(3, 4)
    u = v.unitized()
    assert approx(u.length, 1.0)
    assert approx(u.x, 0.6) and approx(u.y, 0.8)
    assert approx(v.length, 5.0), "unitized() must not modify the original."


def test_unitizing_a_zero_vector_raises():
    """a zero-length vector cannot be unitized"""
    with pytest.raises(ValueError):
        Vector2D(0, 0).unitized()


# --- 2. Rectangle -----------------------------------------------------------

def test_rectangle_area_and_perimeter_are_properties():
    """r.area and r.perimeter need no parentheses"""
    r = Rectangle(3, 4)
    assert approx(r.area, 12)
    assert approx(r.perimeter, 14)


def test_rectangle_properties_track_changes():
    """changing .width updates .area"""
    r = Rectangle(3, 4)
    r.width = 10
    assert approx(r.area, 40), "area is stale -- derive it, do not store it."


def test_rectangle_contains_points():
    """contains() is true inside and on the boundary, false outside"""
    r = Rectangle(4, 2, x=1, y=1)     # spans x 1..5, y 1..3
    assert r.contains(2, 2) is True
    assert r.contains(1, 1) is True, "a point on the corner counts as inside"
    assert r.contains(5, 3) is True, "the far corner counts as inside"
    assert r.contains(0, 2) is False
    assert r.contains(2, 9) is False


def test_rectangle_repr():
    """repr(Rectangle(3, 4)) is 'Rectangle(3, 4, at (0, 0))'"""
    assert repr(Rectangle(3, 4)) == "Rectangle(3, 4, at (0, 0))"


def test_rectangle_rejects_impossible_dimensions():
    """a rectangle with a zero or negative side cannot be constructed"""
    with pytest.raises(ValueError):
        Rectangle(0, 5)
    with pytest.raises(ValueError):
        Rectangle(5, -1)


# --- 3. Square --------------------------------------------------------------

def test_square_is_a_rectangle():
    """Square inherits from Rectangle"""
    assert isinstance(Square(3), Rectangle)


def test_square_sides_are_equal():
    """Square(5) is 5 wide and 5 tall"""
    s = Square(5)
    assert approx(s.width, 5) and approx(s.height, 5)


def test_square_inherits_area_rather_than_redefining_it():
    """Square uses Rectangle's area -- it does not define its own"""
    assert approx(Square(5).area, 25)
    assert "area" not in Square.__dict__, (
        "Square defines its own `area`. It should inherit Rectangle's -- a "
        "second copy of the same formula is a second thing that can go wrong."
    )


def test_square_accepts_a_position():
    """Square(5, x=2, y=3) is positioned like a Rectangle"""
    s = Square(5, x=2, y=3)
    assert (s.x, s.y) == (2, 3)


# --- 4. Wall ----------------------------------------------------------------

def test_wall_height_is_a_property():
    """wall.height is n_courses * course_height, without parentheses"""
    assert approx(Wall(8, course_height=0.2).height, 1.6)


def test_wall_builds_one_box_per_course():
    """to_boxes() returns n_courses COMPAS Boxes"""
    boxes = Wall(5).to_boxes()
    assert len(boxes) == 5
    assert all(isinstance(b, cg.Box) for b in boxes)


def test_wall_geometry_matches_the_week_six_rules():
    """courses stack from z=0 with no gaps, odd ones offset"""
    wall = Wall(4, course_height=0.25, offset=0.1)
    boxes = wall.to_boxes()
    for i, box in enumerate(boxes):
        assert approx(min(c.z for c in box.points), i * 0.25)
        expected_x = 0.1 if i % 2 else 0.0
        assert approx(box.frame.point.x, expected_x)


def test_wall_height_agrees_with_the_geometry_it_builds():
    """the derived height matches the boxes actually produced"""
    wall = Wall(7, course_height=0.3)
    measured = max(c.z for b in wall.to_boxes() for c in b.points)
    assert approx(wall.height, measured)


def test_wall_repr():
    """repr(Wall(8)) is 'Wall(8 courses, 1.60 m tall)'"""
    assert repr(Wall(8, course_height=0.2)) == "Wall(8 courses, 1.60 m tall)"


def test_wall_rejects_nonsense():
    """Wall(0) raises ValueError from the constructor"""
    with pytest.raises(ValueError):
        Wall(0)


def test_tasks_file_stays_pure():
    """tasks.py imports no viewer, files or Rhino -- classes live in the core too"""
    tree = ast.parse((HERE / "tasks.py").read_text())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    forbidden = {"compas_viewer", "json", "os", "sys", "pathlib",
                 "rhinoscriptsyntax", "Rhino", "scriptcontext"}
    leaked = names & forbidden
    assert not leaked, (
        f"tasks.py imports {sorted(leaked)}. Wrapping geometry in a class does "
        "not change which layer it belongs to -- this is still the core."
    )
