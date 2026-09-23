# STARTER FILE — READ ONLY.
#
# `checkpoints/conftest.py` copied me to  answers.py  on first run.
# Edit that file, not this one. If you delete answers.py, the next
# `uv run check.py NN` will regenerate it from this starter.

"""
Week 02 checkpoints — values, types, lists, functions.

In  answers.py  (auto-copied from this starter), replace each
`raise NotImplementedError(...)` with a real implementation, then run from the repository root:

    uv run check.py 02

The precise specification for each function is in `spec/test_tasks.py` (one
folder down, marked READ ONLY). Read it. It answers the questions this
docstring leaves open.
"""


def rectangle_area(width, height):
    """Return the area of a rectangle.

    Parameters
    ----------
    width : float   -- the horizontal dimension
    height : float  -- the vertical dimension

    Returns
    -------
    float -- width * height

    Hint: the whole body is one line. The trap is writing `print` instead of
    `return` -- see section 8 of the README.
    """
    raise NotImplementedError("rectangle_area")


def celsius_to_fahrenheit(celsius):
    """Convert a temperature from Celsius to Fahrenheit.

    The formula is:  F = C * 9/5 + 32

    Parameters
    ----------
    celsius : float

    Returns
    -------
    float

    Hint: in Python 3, `9/5` is 1.8, not 1. Section 5 of the README explains
    why that is worth checking rather than assuming.
    """
    raise NotImplementedError("celsius_to_fahrenheit")


def describe_box(width, height, depth):
    """Return a one-line human-readable description of a box.

    For width=2, height=3, depth=4 the result must be EXACTLY:

        "Box 2.00 x 3.00 x 4.00 m, volume 24.00 m3"

    Note the format: every number shown with exactly two decimal places.

    Returns
    -------
    str

    Hint: f-strings, and the `:.2f` format specifier. README section 6.
    """
    raise NotImplementedError("describe_box")


def every_other(items):
    """Return a new list containing every second element, starting with the first.

    every_other([0, 1, 2, 3, 4, 5])  ->  [0, 2, 4]
    every_other(["a", "b", "c"])     ->  ["a", "c"]

    Returns
    -------
    list

    Hint: this is one slice. You should not need a loop -- and you have not
    been taught loops yet, so if you find yourself wanting one, reread
    README section 7 on slicing.
    """
    raise NotImplementedError("every_other")


def list_stats(numbers):
    """Return (smallest, largest, mean) for a list of numbers.

    list_stats([1, 2, 3, 4])  ->  (1, 4, 2.5)

    The empty list is a real case you must decide about. This specification
    decides for you: see `test_list_stats_handles_the_empty_list` in
    `spec/test_tasks.py` before you implement this.

    Returns
    -------
    tuple -- (min, max, mean)

    Hint: `min()`, `max()`, `sum()` and `len()` are built in. Returning several
    values at once is just `return a, b, c`.
    """
    raise NotImplementedError("list_stats")
