"""
An EXECUTABLE SPEC, written by the human planner.

There is no wall.py yet. These tests define what a correct
`running_bond_wall()` must do -- before any implementation exists.
In `tdd_agent.py` a coder agent will write wall.py and iterate until
this file passes. The tests are the contract; whoever (or whatever)
writes the implementation, the standard of "done" does not move.

Spec: running_bond_wall(length, height, brick=(0.24, 0.115, 0.06), joint=0.01)

- Builds a straight wall along the x-axis starting at x=0, on the ground.
- A course (row) is `brick_height + joint` tall; build as many full
  courses as fit within `height`.
- Bricks in a course are separated by `joint`; as many full bricks as
  fit within `length`. No brick may stick out past [0, length].
- RUNNING BOND: each course is offset from the one below by half a
  module (half of brick_length + joint), so vertical joints never align.
- Returns a list of compas Box objects.
"""

import pytest

from wall import running_bond_wall

LENGTH, HEIGHT = 3.0, 1.0
BRICK = (0.24, 0.115, 0.06)   # length, depth, height (m)
JOINT = 0.01
COURSE_H = BRICK[2] + JOINT
TOL = 1e-6


@pytest.fixture
def bricks():
    return running_bond_wall(LENGTH, HEIGHT, BRICK, JOINT)


def courses(bricks):
    """Group bricks by course index, computed from their center z."""
    by_course = {}
    for box in bricks:
        idx = round((box.frame.point.z - BRICK[2] / 2) / COURSE_H)
        by_course.setdefault(idx, []).append(box)
    return by_course


def test_returns_boxes(bricks):
    assert len(bricks) > 0
    from compas.geometry import Box
    assert all(isinstance(b, Box) for b in bricks)


def test_number_of_courses(bricks):
    expected = int(HEIGHT // COURSE_H)
    assert len(courses(bricks)) == expected


def test_bricks_sit_exactly_on_their_course(bricks):
    for box in bricks:
        bottom = box.frame.point.z - box.zsize / 2
        # bottom must be a whole number of courses above the ground
        assert bottom / COURSE_H == pytest.approx(round(bottom / COURSE_H), abs=1e-6)


def test_nothing_sticks_out_of_the_wall(bricks):
    for box in bricks:
        start = box.frame.point.x - box.xsize / 2
        end = box.frame.point.x + box.xsize / 2
        assert start >= -TOL
        assert end <= LENGTH + TOL


def test_no_overlaps_within_a_course(bricks):
    for course in courses(bricks).values():
        course = sorted(course, key=lambda b: b.frame.point.x)
        for a, b in zip(course, course[1:]):
            end_of_a = a.frame.point.x + a.xsize / 2
            start_of_b = b.frame.point.x - b.xsize / 2
            assert start_of_b >= end_of_a - TOL


def test_running_bond_vertical_joints_never_align(bricks):
    by_course = courses(bricks)
    for idx in range(len(by_course) - 1):
        below = [b.frame.point.x for b in by_course[idx]]
        above = [b.frame.point.x for b in by_course[idx + 1]]
        for xa in above:
            for xb in below:
                assert abs(xa - xb) > TOL, (
                    f"brick centers align between course {idx} and {idx + 1} at x={xa}"
                )
