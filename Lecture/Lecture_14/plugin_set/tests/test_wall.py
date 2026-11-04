"""Executable spec for running_bond_wall — properties, not pictures."""

import math

import pytest
from compas.geometry import Box

from compas_studio import running_bond_wall

TOL = 1e-9


def test_returns_boxes():
    """the wall is a list of COMPAS Boxes"""
    wall = running_bond_wall(2.0, 1.0)
    assert wall and all(isinstance(b, Box) for b in wall)


def test_courses_stack_from_the_ground():
    """the lowest brick sits on z = 0"""
    wall = running_bond_wall(2.0, 1.0)
    assert abs(min(c.z for b in wall for c in b.points)) < TOL


def test_no_brick_sticks_out_past_the_length():
    """every brick lies fully within [0, length]"""
    length = 2.0
    for b in running_bond_wall(length, 1.0):
        xs = [c.x for c in b.points]
        assert min(xs) > -TOL and max(xs) < length + TOL


def test_odd_courses_are_offset():
    """odd courses start half a module further along x than even ones"""
    wall = running_bond_wall(2.0, 0.3, brick=(0.24, 0.115, 0.06), joint=0.01)
    module = 0.24 + 0.01
    by_course = {}
    for b in wall:
        by_course.setdefault(round(b.frame.point.z, 5), []).append(b.frame.point.x)
    zs = sorted(by_course)
    first_of = [min(by_course[z]) for z in zs]
    assert abs((first_of[1] - first_of[0]) - module / 2) < TOL


def test_rejects_nonsense_input():
    """impossible dimensions raise instead of returning junk"""
    with pytest.raises(ValueError):
        running_bond_wall(0, 1.0)
    with pytest.raises(ValueError):
        running_bond_wall(2.0, -1.0)
