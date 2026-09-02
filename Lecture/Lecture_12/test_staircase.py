"""
Unit tests = the SPECIFICATION of the staircase, written as code.

Each test states one fact that must be true for EVERY valid staircase.
Run them with:

    pytest test_staircase.py -v

Two ideas matter here:

1. Test PROPERTIES, not pictures. We cannot assert "it looks like a
   staircase", but we can assert countable, measurable facts: number of
   steps, total height, nothing floating, steps actually ascending.
   If all the invariants hold, the picture takes care of itself.

2. Never compare floats with ==. Computed geometry carries floating-point
   noise; use pytest.approx (or an explicit tolerance) instead.
"""

import pytest

from staircase import straight_staircase

# One typical configuration used by most tests.
N, RISE, TREAD, WIDTH = 8, 0.15, 0.3, 1.2


@pytest.fixture
def steps():
    return straight_staircase(N, RISE, TREAD, WIDTH)


def test_step_count(steps):
    assert len(steps) == N


def test_total_height(steps):
    top = max(box.frame.point.z + box.zsize / 2 for box in steps)
    assert top == pytest.approx(N * RISE)


def test_every_step_rests_on_the_ground(steps):
    # solid staircase: every box's bottom face sits at z = 0
    for box in steps:
        bottom = box.frame.point.z - box.zsize / 2
        assert bottom == pytest.approx(0.0)


def test_steps_ascend_monotonically(steps):
    heights = [box.zsize for box in steps]
    assert heights == sorted(heights)
    # and each step is exactly one rise taller than the previous
    for a, b in zip(heights, heights[1:]):
        assert b - a == pytest.approx(RISE)


def test_no_gap_between_treads(steps):
    # consecutive steps must touch in x: end of one = start of the next
    for a, b in zip(steps, steps[1:]):
        end_of_a = a.frame.point.x + a.xsize / 2
        start_of_b = b.frame.point.x - b.xsize / 2
        assert end_of_a == pytest.approx(start_of_b)


def test_rejects_nonsense_input():
    # good functions fail LOUDLY on invalid input instead of returning junk
    with pytest.raises(ValueError):
        straight_staircase(0, RISE, TREAD, WIDTH)
