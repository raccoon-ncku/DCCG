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
The SPECIFICATION for Week 05.

Every geometric assertion here compares with a TOLERANCE, never with ==.
Rotations run through sines and cosines, and `cos(pi/2)` is 6.1e-17 rather
than 0. Code that demands exact equality on computed geometry does not work,
anywhere, ever.
"""

import math

import compas.geometry as cg

from answers import (
    box_on_ground,
    flatten_to_xy,
    grid_of_boxes,
    move,
    rotate_point_about_z,
)

TOL = 1e-9


def approx(a, b, tol=TOL):
    return abs(a - b) < tol


# --- 1. box_on_ground -------------------------------------------------------

def test_box_on_ground_has_the_right_size():
    """box_on_ground() returns a cube of the requested edge length"""
    box = box_on_ground(0, 0, 2)
    assert isinstance(box, cg.Box)
    assert approx(box.xsize, 2) and approx(box.ysize, 2) and approx(box.zsize, 2)


def test_box_on_ground_actually_sits_on_the_ground():
    """the box's lowest face is at z = 0, not below it"""
    box = box_on_ground(0, 0, 2)
    lowest = min(corner.z for corner in box.points)
    assert approx(lowest, 0.0), (
        f"The bottom of the box is at z={lowest}, not 0. A COMPAS Box is "
        "CENTRED on its frame -- so its frame has to sit half a height up."
    )


def test_box_on_ground_is_positioned_over_xy():
    """the box is centred above the (x, y) it was given"""
    box = box_on_ground(5, -3, 1)
    assert approx(box.frame.point.x, 5)
    assert approx(box.frame.point.y, -3)


def test_box_on_ground_works_for_any_size():
    """the rule holds for other sizes too, not just the one you tested"""
    for size in (0.5, 1.0, 3.7):
        box = box_on_ground(0, 0, size)
        assert approx(min(c.z for c in box.points), 0.0), (
            f"size={size} does not sit on the ground. Did you hard-code the lift?"
        )


# --- 2. move ----------------------------------------------------------------

def test_move_shifts_the_shape():
    """move() offsets the shape by the given amounts"""
    box = cg.Box(1, 1, 1)
    moved = move(box, 3, 4, 5)
    assert approx(moved.frame.point.x, 3)
    assert approx(moved.frame.point.y, 4)
    assert approx(moved.frame.point.z, 5)


def test_move_does_not_modify_the_original():
    """move() leaves the shape it was given exactly where it was"""
    box = cg.Box(1, 1, 1)
    move(box, 3, 4, 5)
    assert approx(box.frame.point.x, 0), (
        "The original box moved. You used .transform() (in place) where you "
        "wanted .transformed() (returns a copy)."
    )


# --- 3. rotate_point_about_z ------------------------------------------------

def test_rotate_point_ninety_degrees():
    """rotating (1,0,0) by 90 degrees gives (0,1,0)"""
    result = rotate_point_about_z(cg.Point(1, 0, 0), 90)
    assert approx(result.x, 0), (
        f"x should be ~0 but is {result.x}. If it is about 0.45, you passed "
        "degrees straight into COMPAS -- it expects radians."
    )
    assert approx(result.y, 1)


def test_rotate_point_full_turn_returns_to_start():
    """rotating by 360 degrees comes back to where it started"""
    result = rotate_point_about_z(cg.Point(2, 1, 3), 360)
    assert approx(result.x, 2) and approx(result.y, 1) and approx(result.z, 3)


def test_rotate_point_preserves_z_and_distance():
    """rotation about Z keeps the height and the distance from the axis"""
    start = cg.Point(3, 4, 7)
    result = rotate_point_about_z(start, 37)
    assert approx(result.z, 7), "Rotating about Z must not change z."
    assert approx(math.hypot(result.x, result.y), math.hypot(3, 4)), (
        "The point changed its distance from the Z axis -- that is a scale, "
        "not a rotation."
    )


def test_rotate_point_does_not_modify_the_original():
    """rotate_point_about_z() returns a new Point"""
    start = cg.Point(1, 0, 0)
    rotate_point_about_z(start, 90)
    assert approx(start.x, 1), "The original Point was rotated in place."


# --- 4. grid_of_boxes -------------------------------------------------------

def test_grid_has_the_right_number_of_boxes():
    """grid_of_boxes() returns nx * ny boxes"""
    assert len(grid_of_boxes(3, 4, 2.0, 1.0)) == 12
    assert len(grid_of_boxes(1, 1, 2.0, 1.0)) == 1


def test_grid_spacing_and_extent():
    """the grid starts at (0,0) and the last box is at ((nx-1)*s, (ny-1)*s)"""
    boxes = grid_of_boxes(3, 2, 2.0, 1.0)
    first, last = boxes[0], boxes[-1]
    assert approx(first.frame.point.x, 0) and approx(first.frame.point.y, 0)
    assert approx(last.frame.point.x, 4.0), "3 columns, 2.0 apart: last x is 4.0"
    assert approx(last.frame.point.y, 2.0), "2 rows, 2.0 apart: last y is 2.0"


def test_grid_is_ordered_with_x_changing_fastest():
    """the second box is the next one along x, not along y"""
    boxes = grid_of_boxes(3, 2, 2.0, 1.0)
    assert approx(boxes[1].frame.point.x, 2.0), (
        "boxes[1] should be the next column. Your loops are nested the other "
        "way round -- the OUTER loop should be y."
    )
    assert approx(boxes[1].frame.point.y, 0.0)


def test_every_box_in_the_grid_sits_on_the_ground():
    """the grid inherits the ground rule from checkpoint 1"""
    for box in grid_of_boxes(2, 2, 2.0, 1.5):
        assert approx(min(c.z for c in box.points), 0.0)


# --- 5. flatten_to_xy -------------------------------------------------------

def test_flatten_sets_z_to_zero():
    """flatten_to_xy() drops every point onto the ground plane"""
    result = flatten_to_xy([cg.Point(1, 2, 9), cg.Point(-3, 0, -4)])
    assert [(p.x, p.y, p.z) for p in result] == [(1, 2, 0), (-3, 0, 0)]


def test_flatten_keeps_the_order_and_count():
    """flatten_to_xy() returns as many points as it was given, in order"""
    points = [cg.Point(i, 0, i) for i in range(5)]
    result = flatten_to_xy(points)
    assert len(result) == 5
    assert [p.x for p in result] == [0, 1, 2, 3, 4]


def test_flatten_does_not_modify_the_input_points():
    """the Points passed in still have their original z"""
    points = [cg.Point(1, 2, 9)]
    flatten_to_xy(points)
    assert approx(points[0].z, 9), (
        "You edited the caller's Points. Setting p.z = 0 changes the object "
        "everyone else is still holding -- build new Points instead."
    )


def test_flatten_of_nothing_is_nothing():
    """flatten_to_xy([]) is []"""
    assert flatten_to_xy([]) == []
