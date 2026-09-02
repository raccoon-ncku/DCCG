"""A straight staircase, as a pure geometry function."""

from compas.geometry import Box, Frame


def straight_staircase(n_steps, rise=0.17, tread=0.28, width=1.0):
    """A solid straight staircase built from stacked boxes.

    Each step is one box sitting on the ground and rising to its full height,
    like a staircase cut from solid material.

    Parameters
    ----------
    n_steps : int   -- number of steps (at least 1)
    rise : float    -- height gained per step, m
    tread : float   -- depth of each step along x, m
    width : float   -- width of the staircase along y, m

    Returns
    -------
    list[compas.geometry.Box] -- bottom step first

    Raises
    ------
    ValueError -- if n_steps < 1, or any dimension is not positive
    """
    if n_steps < 1:
        raise ValueError("a staircase needs at least one step")
    if min(rise, tread, width) <= 0:
        raise ValueError("rise, tread and width must all be positive")

    steps = []
    for i in range(n_steps):
        height = (i + 1) * rise
        center_x = i * tread + tread / 2
        frame = Frame([center_x, 0.0, height / 2], [1, 0, 0], [0, 1, 0])
        steps.append(Box(tread, width, height, frame=frame))
    return steps
