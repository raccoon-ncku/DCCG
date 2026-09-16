# ──────────────────────────────────────────────────────────────────────────────
#  READ ONLY  ·  this file is the SPEC, not the answers.
#
#  If a checkpoint fails, edit `../tasks.py` (or `../core.py` / `../runner.py`
#  in Week 06), NOT this file. Read the assertions below to understand what
#  each checkpoint is checking; do not change them.
# ──────────────────────────────────────────────────────────────────────────────
"""
The SPECIFICATION for Week 08.

Note what the geometry tests check: COUNTS and LENGTHS and RELATIONSHIPS.
None of them looks at a picture, because a picture cannot tell you that you
produced 121 branches where you meant 127.

`test_tree_is_pure_between_calls` is the one to read twice. It calls the
function on the same input and checks that the answer does not change. That
sounds trivially true -- and it is exactly what breaks the moment you
accumulate into a list defined outside the function.
"""

import math

import compas.geometry as cg
import pytest

from tasks import factorial, flatten, sierpinski, tree_segments

TOL = 1e-9
A = cg.Point(0, 0, 0)
B = cg.Point(4, 0, 0)
C = cg.Point(0, 4, 0)


def approx(a, b, tol=TOL):
    return abs(a - b) < tol


# --- 1. factorial -----------------------------------------------------------

def test_factorial_known_values():
    """factorial() computes 0!, 1!, 5! and 10! correctly"""
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(10) == 3628800


def test_factorial_rejects_negative_input():
    """factorial(-1) raises ValueError instead of recursing forever"""
    with pytest.raises(ValueError):
        factorial(-1)


# --- 2. flatten -------------------------------------------------------------

def test_flatten_one_level():
    """flatten() unpacks a single level of nesting"""
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]


def test_flatten_deep_nesting():
    """flatten() handles nesting of any depth"""
    assert flatten([1, [2, [3, [4, [5]]]]]) == [1, 2, 3, 4, 5]


def test_flatten_edge_cases():
    """flatten() copes with empty lists at any position"""
    assert flatten([]) == []
    assert flatten([[], [1], [[], [2]]]) == [1, 2]


def test_flatten_preserves_order():
    """flatten() keeps the left-to-right order of the original"""
    assert flatten([[3, 1], [2, [9, 4]]]) == [3, 1, 2, 9, 4]


# --- 3. sierpinski ----------------------------------------------------------

def test_sierpinski_depth_zero_is_the_triangle_itself():
    """depth 0 returns exactly one triangle: the input"""
    result = sierpinski(A, B, C, 0)
    assert len(result) == 1
    assert len(result[0]) == 3


def test_sierpinski_triangle_count_is_three_to_the_depth():
    """depth d produces 3**d triangles"""
    for depth in range(5):
        assert len(sierpinski(A, B, C, depth)) == 3 ** depth, (
            f"depth {depth} should give {3 ** depth} triangles. If you got "
            f"{4 ** depth}, you are recursing into the middle triangle too -- "
            "that one is the hole."
        )


def test_sierpinski_halves_the_edge_length_each_level():
    """every triangle at depth 1 has edges half the length of the original"""
    for triangle in sierpinski(A, B, C, 1):
        p, q, r = triangle
        edge = p.distance_to_point(q)
        assert approx(edge, 2.0), (
            f"edge length {edge}, expected 2.0 (half of the original 4.0)"
        )


def test_sierpinski_total_area_shrinks_by_three_quarters():
    """each level keeps 3/4 of the previous total area (a property test)"""
    def area(tri):
        p, q, r = tri
        return abs(cg.Vector(*(q - p)).cross(cg.Vector(*(r - p))).length) / 2

    previous = sum(area(t) for t in sierpinski(A, B, C, 0))
    for depth in range(1, 4):
        total = sum(area(t) for t in sierpinski(A, B, C, depth))
        assert approx(total, previous * 0.75), (
            f"depth {depth}: total area {total}, expected {previous * 0.75}"
        )
        previous = total


def test_sierpinski_rejects_negative_depth():
    """a negative depth raises ValueError"""
    with pytest.raises(ValueError):
        sierpinski(A, B, C, -1)


# --- 4. tree_segments -------------------------------------------------------

def test_tree_depth_zero_is_empty():
    """a tree of depth 0 has no segments at all"""
    assert tree_segments(1.0, 30, 0) == []


def test_tree_depth_one_is_a_single_trunk():
    """depth 1 is one segment, from the origin straight up"""
    segments = tree_segments(2.0, 30, 1)
    assert len(segments) == 1
    start, end = segments[0]
    assert approx(start.x, 0) and approx(start.y, 0)
    assert approx(end.x, 0), "the trunk should be vertical"
    assert approx(end.y, 2.0), "the trunk should be `length` long"


def test_tree_segment_count_doubles_each_level():
    """a tree of depth d has 2**d - 1 segments"""
    for depth in range(1, 8):
        expected = 2 ** depth - 1
        actual = len(tree_segments(1.0, 25, depth))
        assert actual == expected, (
            f"depth {depth}: got {actual} segments, expected {expected}. "
            "Every branch tip must spawn exactly two children."
        )


def test_tree_branches_shrink_by_the_scale_factor():
    """each generation is `scale` times the length of the one before"""
    segments = tree_segments(1.0, 30, 3, scale=0.5)
    lengths = sorted({round(s.distance_to_point(e), 6) for s, e in segments})
    assert lengths == [0.25, 0.5, 1.0], (
        f"found branch lengths {lengths}, expected [0.25, 0.5, 1.0]"
    )


def test_tree_branches_actually_branch():
    """the two children of the trunk go to different places"""
    segments = tree_segments(1.0, 30, 2)
    tips = [(round(e.x, 6), round(e.y, 6)) for _, e in segments]
    assert len(set(tips)) == 3, (
        "The branches all ended in the same place -- the angle is not being "
        "applied, or it is being applied in the same direction twice."
    )


def test_tree_children_start_where_the_parent_ended():
    """no branch floats away from its parent"""
    segments = tree_segments(1.0, 30, 3)
    starts = {(round(s.x, 6), round(s.y, 6)) for s, _ in segments}
    ends = {(round(e.x, 6), round(e.y, 6)) for _, e in segments}
    origin = (0.0, 0.0)
    orphans = starts - ends - {origin}
    assert not orphans, f"these branches start nowhere: {orphans}"


def test_tree_is_pure_between_calls():
    """calling tree_segments twice gives the same answer both times"""
    # If your function appends into a list defined OUTSIDE it, the second call
    # returns the first call's segments as well and this fails. Same bug as the
    # mutable default argument in Week 04, wearing different clothes.
    first = tree_segments(1.0, 30, 4)
    second = tree_segments(1.0, 30, 4)
    assert len(first) == len(second) == 15, (
        f"first call gave {len(first)} segments, second gave {len(second)}. "
        "State is leaking between calls -- return a new list from each call "
        "instead of appending into a shared one."
    )


def test_tree_rejects_negative_depth():
    """a negative depth raises ValueError"""
    with pytest.raises(ValueError):
        tree_segments(1.0, 30, -1)
