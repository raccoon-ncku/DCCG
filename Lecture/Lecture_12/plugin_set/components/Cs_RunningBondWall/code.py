"""
Grasshopper ADAPTER for compas_studio.running_bond_wall.

This file is the whole point of the course, in miniature. Look how little it
does: it finds the core, takes the Grasshopper inputs, calls ONE function from
the tested core, converts the result to Rhino geometry, and returns it. There
is no geometry logic here to get wrong -- that logic lives in
compas_studio.wall, where pytest has already checked it (headlessly, with no
Rhino in sight).

The block down to the dashed line is the same in every component: it finds
this package's own copy of the core, which ships inside the .yak (in lib/).
ghuser-build fills in {{version}}, so a component always loads the core of
its own release.

ghuser-builder turns this folder into Cs_RunningBondWall.ghuser on Linux, with
Rhino installed nowhere. Keep adapters this thin: an adapter you can read in
ten seconds is an adapter you do not need to test.
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
    raise ImportError(f"{PACKAGE} {VERSION} is not installed; install it with the Package Manager")


_lib = _package_lib()
if _lib not in sys.path:
    sys.path.insert(0, _lib)

# ---------------------------------------------------------------------------
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
