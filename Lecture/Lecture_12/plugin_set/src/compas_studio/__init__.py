"""compas_studio: the pure core of a small Grasshopper plugin set.

Numbers in, COMPAS geometry out. No Rhino, no viewer, no file IO, so it can be
tested anywhere. The components in ../components/ call it and convert the result.
"""

from .wall import running_bond_wall
from .staircase import straight_staircase
from .grid import grid_mesh
from .stud_wall import StudWall

__all__ = ["running_bond_wall", "straight_staircase", "grid_mesh", "StudWall"]
__version__ = "0.1.0"
