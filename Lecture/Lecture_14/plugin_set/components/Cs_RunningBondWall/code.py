"""Grasshopper ADAPTER for compas_studio.running_bond_wall. Thin on purpose.

The block down to the dashed line is the same in every component: it finds
this package's own copy of the core (shipped inside the .yak, in lib/).
"""
# r: compas

import glob
import os
import sys

PACKAGE, VERSION = "compas-studio", "{{version}}"


def _package_lib():
    # Rhino installs packages to <root>/packages/<rhino version>/<name>/<version>/
    roots = [
        os.path.join(os.environ.get("APPDATA", ""), "McNeel", "Rhinoceros", "packages"),
        os.path.expanduser("~/Library/Application Support/McNeel/Rhinoceros/packages"),
    ]
    for root in roots:
        for lib in sorted(glob.glob(os.path.join(root, "*", PACKAGE, VERSION, "lib")), reverse=True):
            return lib
    return None  # not installed: a dev build (scripts/dev.py) imports the core through `# env:`


_lib = _package_lib()
if _lib and _lib not in sys.path:
    sys.path.insert(0, _lib)

# ---------------------------------------------------------------------------
# Placing a component writes type hints into RunScript's signature, such as
# System.Collections.Generic.List[float], Rhino.Geometry.Curve or
# Grasshopper.DataTree[float]: these three names must exist, or it cannot run.
import Grasshopper  # noqa: E402, F401
import Rhino  # noqa: E402, F401
import System  # noqa: E402, F401
from ghpythonlib.componentbase import executingcomponent as component  # noqa: E402

from compas_studio import running_bond_wall  # noqa: E402
from compas_rhino.conversions import box_to_rhino  # noqa: E402


class Cs_RunningBondWall(component):
    def RunScript(self, length, height, brick_length, joint):
        # Grasshopper hands optional inputs in as None -- fall back to the
        # core's own defaults rather than duplicating them here.
        if length is None or height is None:
            return None

        brick = (brick_length, 0.115, 0.06) if brick_length else (0.24, 0.115, 0.06)
        kwargs = {"brick": brick}
        if joint is not None:
            kwargs["joint"] = joint

        boxes = running_bond_wall(length, height, **kwargs)
        bricks = [box_to_rhino(b) for b in boxes]
        return bricks
