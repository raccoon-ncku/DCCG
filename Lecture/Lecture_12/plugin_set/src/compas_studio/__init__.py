"""
compas_studio — a small Grasshopper plugin SET, built the course way.

Everything importable from this package is PURE: numbers in, COMPAS geometry
out. No `import rhinoscriptsyntax`, no `import Rhino`, no viewer, no file IO.
That is what lets this library:

  - be tested headlessly with pytest (see ../tests/), on any machine, in CI;
  - be built into Grasshopper .ghuser components by GitHub Actions, with no
    Rhino installed on the runner;
  - live and be developed entirely outside Rhino, and only *ship* into it.

The Grasshopper components in ../components/ are thin adapters: each one imports
a function from here, calls it, and converts the result to Rhino geometry. All
the intelligence is in this package; the components are boring on purpose.
"""

from .wall import running_bond_wall
from .staircase import straight_staircase
from .grid import grid_mesh

__all__ = ["running_bond_wall", "straight_staircase", "grid_mesh"]
__version__ = "0.1.0"
