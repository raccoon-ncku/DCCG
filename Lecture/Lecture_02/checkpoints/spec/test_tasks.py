# ──────────────────────────────────────────────────────────────────────────────
#  READ ONLY  ·  this file is the SPEC, not the answers.
#
#  If a checkpoint fails, edit `../tasks.py` (or `../core.py` / `../runner.py`
#  in Week 06), NOT this file. Read the assertions below to understand what
#  each checkpoint is checking; do not change them.
# ──────────────────────────────────────────────────────────────────────────────
"""
The SPECIFICATION for Week 02.

Read this file. Each test states one fact that must be true about your code.
Where the task docstring was vague, this file is precise -- that is the
division of labour between prose and a spec, and it is the reason Week 10
exists.
"""

import pytest

from tasks import (
    celsius_to_fahrenheit,
    describe_box,
    every_other,
    list_stats,
    rectangle_area,
)


def test_rectangle_area_multiplies():
    """rectangle_area() returns width * height"""
    assert rectangle_area(3, 4) == 12
    assert rectangle_area(2.5, 4) == 10


def test_rectangle_area_returns_rather_than_prints():
    """rectangle_area() RETURNS the value (does not just print it)"""
    result = rectangle_area(3, 4)
    assert result is not None, (
        "Your function printed the answer instead of returning it. "
        "print() shows a value; return hands it back to the caller."
    )


def test_celsius_to_fahrenheit_known_values():
    """celsius_to_fahrenheit() converts correctly at 0, 100 and 37 degrees"""
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212
    # 37 C is 98.6 F -- and this is a float, so compare with a tolerance,
    # never with ==. See the float warning in the README.
    assert abs(celsius_to_fahrenheit(37) - 98.6) < 1e-9


def test_describe_box_exact_format():
    """describe_box() produces the exact specified string"""
    assert describe_box(2, 3, 4) == "Box 2.00 x 3.00 x 4.00 m, volume 24.00 m3"


def test_describe_box_always_two_decimals():
    """describe_box() pads and rounds to exactly two decimal places"""
    assert describe_box(1, 1, 1) == "Box 1.00 x 1.00 x 1.00 m, volume 1.00 m3"
    assert describe_box(0.25, 0.5, 2) == "Box 0.25 x 0.50 x 2.00 m, volume 0.25 m3"


def test_every_other_picks_alternate_items():
    """every_other() returns items 0, 2, 4, ..."""
    assert every_other([0, 1, 2, 3, 4, 5]) == [0, 2, 4]
    assert every_other(["a", "b", "c"]) == ["a", "c"]
    assert every_other([]) == []


def test_every_other_does_not_modify_its_input():
    """every_other() leaves the original list untouched"""
    original = [0, 1, 2, 3]
    every_other(original)
    assert original == [0, 1, 2, 3], (
        "Your function changed the list it was given. A function that quietly "
        "modifies its input is a bug waiting to happen -- return a new list."
    )


def test_list_stats_returns_min_max_mean():
    """list_stats() returns (min, max, mean) as a 3-tuple"""
    assert list_stats([1, 2, 3, 4]) == (1, 4, 2.5)
    assert list_stats([5]) == (5, 5, 5.0)


def test_list_stats_handles_the_empty_list():
    """list_stats([]) raises ValueError rather than returning nonsense"""
    # THIS is the decision the task docstring left open. An empty list has no
    # minimum, so there is no honest value to return. Returning 0 or None would
    # be a lie that shows up much later, somewhere else, as a confusing bug.
    # Refusing loudly is better than answering wrongly.
    with pytest.raises(ValueError):
        list_stats([])
