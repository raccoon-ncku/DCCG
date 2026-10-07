"""Life-like cellular automata (B3/S23 by default) and voxel towers.

Neighbours are counted with eight shifted copies of a numpy array; step()
returns a new grid (never update in place); the border is dead, not wrapped.
Stacking generations as floors turns a 2D rule into a 3D form.
W11 simulation README §1.
"""

import numpy as np


def neighbours(grid):
    """Number of live neighbours of every cell (dead border)."""
    g = np.pad(grid.astype(np.int8), 1)
    n = np.zeros_like(grid, dtype=np.int8)
    h, w = grid.shape
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx or dy:
                n += g[1 + dy:1 + dy + h, 1 + dx:1 + dx + w]
    return n


def step(grid, born=(3,), survive=(2, 3)):
    """One generation of a life-like rule ("B3/S23" by default). Returns a new grid."""
    n = neighbours(grid)
    alive = grid.astype(bool)
    return (alive & np.isin(n, survive)) | (~alive & np.isin(n, born))


def run(grid, generations, **rule):
    """[grid, step(grid), step(step(grid)), ...] -- generations + 1 grids."""
    history = [np.asarray(grid, dtype=bool)]
    for _ in range(generations):
        history.append(step(history[-1], **rule))
    return history


def voxels(history):
    """Stack the generations into (x, y, z) voxel centres: generation t is floor t."""
    return [(x, y, z) for z, g in enumerate(history) for y, x in zip(*np.nonzero(g))]


def pattern(rows):
    """A grid from strings: '#' alive, anything else dead."""
    return np.array([[c == "#" for c in row] for row in rows], dtype=bool)
