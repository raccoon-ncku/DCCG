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
The SPECIFICATION for Week 03.

Notice `test_circle_points_lie_on_the_circle`: it does not check the exact
coordinates it expects. It checks a PROPERTY -- every point is `radius` away
from the centre. That style of test is the whole subject of Week 10, and it is
the only way to test geometry that carries floating-point noise.
"""

import math

from answers import (
    circle_points,
    fizz_buzz,
    is_palindrome,
    primes_below,
    roll_dice,
    triangle,
)


def test_fizz_buzz_small_case():
    """fizz_buzz(5) gives the expected five strings"""
    assert fizz_buzz(5) == ["1", "2", "Fizz", "4", "Buzz"]


def test_fizz_buzz_handles_fifteen():
    """fizz_buzz() returns 'FizzBuzz' for multiples of both 3 and 5"""
    result = fizz_buzz(15)
    assert len(result) == 15, "fizz_buzz(n) must return n items (1..n inclusive)"
    assert result[14] == "FizzBuzz", (
        "15 is divisible by 3 and by 5. If you got 'Fizz', your first branch "
        "caught it before the combined case could -- branch order matters."
    )


def test_fizz_buzz_returns_strings():
    """fizz_buzz() returns strings, not a mix of ints and strings"""
    assert all(isinstance(item, str) for item in fizz_buzz(10))


def test_triangle_shape():
    """triangle(3) is three rows of 1, 2 and 3 asterisks"""
    assert triangle(3) == "*\n**\n***"


def test_triangle_has_no_trailing_newline():
    """triangle() does not end with a newline"""
    assert triangle(1) == "*"
    assert not triangle(4).endswith("\n")


def test_is_palindrome_simple_words():
    """is_palindrome() works on single words, ignoring case"""
    assert is_palindrome("abba") is True
    assert is_palindrome("Racecar") is True
    assert is_palindrome("hello") is False


def test_is_palindrome_ignores_spaces():
    """is_palindrome() ignores spaces in phrases"""
    assert is_palindrome("never odd or even") is True
    assert is_palindrome("A man a plan a canal Panama") is True
    assert is_palindrome("never even or odd") is False


def test_is_palindrome_edge_cases():
    """is_palindrome() treats the empty string and single letters as palindromes"""
    assert is_palindrome("") is True
    assert is_palindrome("a") is True


def test_primes_below_ten():
    """primes_below(10) is [2, 3, 5, 7]"""
    assert primes_below(10) == [2, 3, 5, 7]


def test_primes_below_excludes_zero_and_one():
    """primes_below() never includes 0 or 1 -- neither is prime"""
    assert primes_below(2) == []
    assert primes_below(3) == [2]


def test_primes_below_fifty():
    """primes_below(50) finds all 15 primes below 50"""
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    assert primes_below(50) == expected


def test_circle_points_count_and_first_point():
    """circle_points() returns `count` points, starting at (radius, 0)"""
    points = circle_points(4, 2.0)
    assert len(points) == 4
    x, y = points[0]
    assert abs(x - 2.0) < 1e-9
    assert abs(y - 0.0) < 1e-9


def test_circle_points_lie_on_the_circle():
    """every point returned is exactly `radius` from the centre (a property test)"""
    radius = 3.0
    for x, y in circle_points(12, radius):
        distance = math.sqrt(x * x + y * y)
        assert abs(distance - radius) < 1e-9, (
            f"point ({x}, {y}) is {distance} from the origin, not {radius}"
        )


def test_circle_points_go_counter_clockwise():
    """circle_points() advances counter-clockwise (the second point has positive y)"""
    points = circle_points(4, 1.0)
    assert points[1][1] > 0, (
        "The second point should be at 90 degrees, i.e. near (0, 1). "
        "A negative y means you are going clockwise."
    )


def test_roll_dice_is_reproducible():
    """the same seed always produces the same rolls"""
    assert roll_dice(42, 10) == roll_dice(42, 10)


def test_roll_dice_differs_between_seeds():
    """different seeds produce different sequences"""
    assert roll_dice(42, 10) != roll_dice(7, 10)


def test_roll_dice_values_are_valid():
    """every roll is a whole number from 1 to 6"""
    rolls = roll_dice(1, 50)
    assert len(rolls) == 50
    assert all(isinstance(r, int) and 1 <= r <= 6 for r in rolls)
