"""A column grid: the one core function this template ships with.

Replace it with your own. Keep the shape: plain numbers in, COMPAS geometry
out, a ValueError for input that makes no sense.
"""

from compas.geometry import Point


def column_grid(nx, ny, bay=6.0):
    """Column positions on an nx by ny grid of bays.

    Parameters
    ----------
    nx, ny : int
        Number of bays along x and y. At least 1 each.
    bay : float
        Bay size in metres. Positive.

    Returns
    -------
    list[Point]
        (nx + 1) * (ny + 1) points on z = 0, row by row from the origin.
    """
    if nx < 1 or ny < 1:
        raise ValueError(f"need at least one bay each way, got nx={nx}, ny={ny}")
    if bay <= 0:
        raise ValueError(f"bay must be positive, got {bay}")
    return [Point(i * bay, j * bay, 0.0) for j in range(ny + 1) for i in range(nx + 1)]
