"""Executable spec for straight_staircase."""

import pytest
from compas.geometry import Box

from compas_studio import straight_staircase

TOL = 1e-9


def test_step_count():
    """one box per step"""
    assert len(straight_staircase(8)) == 8


def test_steps_ascend_monotonically():
    """each step is taller than the one before"""
    heights = [b.zsize for b in straight_staircase(6, rise=0.17)]
    assert heights == sorted(heights)
    assert all(b > 0 for b in heights)


def test_total_run_equals_steps_times_tread():
    """the staircase is exactly n_steps * tread deep"""
    steps = straight_staircase(5, tread=0.28)
    far = max(c.x for b in steps for c in b.points)
    assert abs(far - 5 * 0.28) < TOL


def test_nothing_floats():
    """every step sits on the ground"""
    for b in straight_staircase(5):
        assert abs(min(c.z for c in b.points)) < TOL


def test_rejects_nonsense_input():
    """zero steps or negative dimensions raise"""
    with pytest.raises(ValueError):
        straight_staircase(0)
    with pytest.raises(ValueError):
        straight_staircase(5, rise=-0.1)
