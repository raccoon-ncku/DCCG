"""
The unit under test: a pure geometry function.

Note what this module does NOT do: no viewer, no file IO, no printing,
no Rhino. It takes numbers in and returns geometry out. Pure functions
like this are easy to test, easy to reuse in Rhino or Grasshopper later,
and easy for an agent (or a classmate) to work on without breaking
anything else. This separation is the core software-engineering habit
of this lecture.
"""

from compas.geometry import Box, Frame


def straight_staircase(n_steps, rise, tread, width):
    """A solid straight staircase built from stacked boxes.

    Each step is one box sitting on the ground and reaching its full
    height, like a staircase cut from solid material.

    Parameters
    ----------
    n_steps : int   -- number of steps
    rise : float    -- height of each step (m)
    tread : float   -- depth of each step in x (m)
    width : float   -- width of the staircase in y (m)

    Returns
    -------
    list[Box]
    """
    if n_steps < 1:
        raise ValueError("a staircase needs at least one step")

    steps = []
    for i in range(n_steps):
        height = (i + 1) * rise                      # step i reaches this height
        center_x = i * tread + tread / 2
        frame = Frame([center_x, 0.0, height / 2], [1, 0, 0], [0, 1, 0])
        steps.append(Box(tread, width, height, frame=frame))
    return steps
