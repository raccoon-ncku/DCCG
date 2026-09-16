"""
Week 03 checkpoints — control flow, modules, functions.

Edit ONLY this file. Run from the repository root:

    uv run check.py 03

`spec/test_tasks.py` (one folder down, marked READ ONLY) is the specification.
Read it whenever a docstring here leaves you guessing -- that is what it is for.
"""

import math
import random


def fizz_buzz(n):
    """Return the FizzBuzz sequence for 1..n as a list of strings.

    For each number from 1 to n inclusive:
      - divisible by 3 AND 5  -> "FizzBuzz"
      - divisible by 3        -> "Fizz"
      - divisible by 5        -> "Buzz"
      - otherwise             -> the number, as a string

    fizz_buzz(5)  ->  ["1", "2", "Fizz", "4", "Buzz"]

    Hint: the order of your if/elif branches matters. Test 15 first, or it
    will never be reached. Note also that every item is a STRING.
    """
    raise NotImplementedError("fizz_buzz")


def triangle(n):
    """Return a left-aligned triangle of asterisks, n rows tall, as one string.

    triangle(3) returns the string:

        *
        **
        ***

    That is: "*\\n**\\n***" -- rows joined by newlines, with NO trailing
    newline at the end.

    Hint: build a list of rows, then "\\n".join(rows). The string "*" * 3 is
    "***", so you may not need a nested loop at all.
    """
    raise NotImplementedError("triangle")


def is_palindrome(text):
    """Return True if `text` reads the same forwards and backwards.

    Spaces and capitalisation are IGNORED:

        is_palindrome("Racecar")                   -> True
        is_palindrome("A man a plan a canal Panama") -> True
        is_palindrome("hello")                     -> False

    Hint: first normalise (lowercase, remove spaces), then compare the result
    with its own reverse. Week 02's slicing section has the reverse trick.
    """
    raise NotImplementedError("is_palindrome")


def primes_below(n):
    """Return a list of all prime numbers strictly less than n, in order.

    primes_below(10)  ->  [2, 3, 5, 7]
    primes_below(2)   ->  []

    A prime is a whole number greater than 1 that is divisible only by 1 and
    itself.

    Hint: for each candidate, try dividing by every number from 2 upward. If
    any divides it evenly, it is not prime -- and you can stop checking that
    candidate immediately (`break`). You only need to test divisors up to the
    square root of the candidate; understanding WHY is the interesting part,
    and it is what earns an A on assignment A1.
    """
    raise NotImplementedError("primes_below")


def circle_points(count, radius):
    """Return `count` points spaced evenly around a circle of the given radius.

    Each point is a tuple (x, y). The first point is at angle 0, i.e. exactly
    (radius, 0.0). Points go counter-clockwise.

    circle_points(4, 1) -> approximately [(1,0), (0,1), (-1,0), (0,-1)]

    Hint: the angle of point i is  i * 2*pi / count  (radians -- see the README
    warning). Then x = radius * cos(angle), y = radius * sin(angle).
    You will get values like 6.1e-17 instead of 0. That is normal, and it is
    why the spec compares with a tolerance instead of ==.
    """
    raise NotImplementedError("circle_points")


def roll_dice(seed, count):
    """Return `count` dice rolls (integers 1-6), reproducibly.

    The same seed must ALWAYS produce the same sequence:

        roll_dice(42, 5) == roll_dice(42, 5)     # always True
        roll_dice(42, 5) != roll_dice(7, 5)      # different seeds differ

    Hint: call random.seed(seed) first, then random.randint(1, 6) `count`
    times. This is the point of the exercise: seeded randomness is repeatable,
    and repeatable means testable. Unrepeatable bugs are the ones that survive.
    """
    raise NotImplementedError("roll_dice")
