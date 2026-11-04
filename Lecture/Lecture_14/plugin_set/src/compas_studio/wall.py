"""A running-bond brick wall, as a pure geometry function.

This is the *reviewed, shippable* version of the wall. Compare it with
`../../wall.py` in this lecture folder -- that one is the unedited output of a
small model: it works, but it is 150 lines of the model arguing with itself in
comments. This one does the same job in 20 readable lines. Same tests pass on
both (see ../tests/test_wall.py). "It passes the tests" is necessary, not
sufficient; a human still has to decide it is *good*. That decision is what
review is.
"""

import math

from compas.geometry import Box, Frame


def running_bond_wall(length, height, brick=(0.24, 0.115, 0.06), joint=0.01):
    """Build a running-bond wall along the x-axis.

    Courses stack in z. Odd courses are shifted by half a module so the vertical
    joints never line up -- that stagger is what "running bond" means. Only full
    bricks that fit entirely within [0, length] are placed.

    Parameters
    ----------
    length : float          -- wall length along x, m
    height : float          -- wall height along z, m
    brick : (float, float, float) -- brick (length, depth, height), m
    joint : float           -- mortar joint thickness, m

    Returns
    -------
    list[compas.geometry.Box] -- bottom course first

    Raises
    ------
    ValueError -- if length, height, or any brick dimension is not positive
    """
    b_len, b_dep, b_hgt = brick
    if min(length, height, b_len, b_dep, b_hgt) <= 0:
        raise ValueError("length, height and brick dimensions must be positive")

    module = b_len + joint           # one brick + one joint, the repeating unit
    course_h = b_hgt + joint
    n_courses = int(height // course_h)

    bricks = []
    for c in range(n_courses):
        offset = module / 2 if c % 2 else 0.0
        z = c * course_h + b_hgt / 2
        # brick k in this course starts at offset + k*module; keep those whose
        # whole footprint lies inside [0, length].
        k = 0
        while offset + k * module + b_len <= length:
            x = offset + k * module + b_len / 2
            frame = Frame([x, b_dep / 2, z], [1, 0, 0], [0, 1, 0])
            bricks.append(Box(b_len, b_dep, b_hgt, frame=frame))
            k += 1
    return bricks
