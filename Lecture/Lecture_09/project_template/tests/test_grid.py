"""The spec for column_grid, written as properties (Week 10).

Read it as the brief: every sentence a client could say about a column grid
is one test here.
"""

import pytest

from my_tool import column_grid


def test_there_is_one_more_column_than_bays_each_way():
    assert len(column_grid(4, 3)) == 5 * 4


def test_neighbouring_columns_are_one_bay_apart():
    points = column_grid(3, 2, bay=7.5)
    assert points[1].x - points[0].x == pytest.approx(7.5)


def test_the_grid_starts_at_the_origin_and_stays_on_the_ground():
    points = column_grid(2, 2)
    assert (points[0].x, points[0].y) == pytest.approx((0.0, 0.0))
    assert all(p.z == pytest.approx(0.0) for p in points)


def test_the_far_corner_is_where_the_bays_say():
    assert (column_grid(4, 3, bay=6.0)[-1].x, column_grid(4, 3, bay=6.0)[-1].y) == pytest.approx((24.0, 18.0))


@pytest.mark.parametrize("nx, ny, bay", [(0, 3, 6.0), (3, 0, 6.0), (3, 3, 0.0), (3, 3, -1.0)])
def test_rejects_nonsense_input(nx, ny, bay):
    with pytest.raises(ValueError):
        column_grid(nx, ny, bay)
