"""Column Grid: the Grasshopper adapter for my_tool.column_grid. Thin on purpose.

Everything above the line of dashes is the same in every component: it finds
this package's own copy of the core (shipped inside the .yak, in lib/) and
puts it on Python's path. ghuser-build fills in {{version}}.
"""
# r: compas

import glob
import os
import sys

PACKAGE, VERSION = "my-tool", "{{version}}"


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
import Rhino.Geometry as rg  # noqa: E402
from ghpythonlib.componentbase import executingcomponent as component  # noqa: E402

from my_tool import column_grid  # noqa: E402


class Mt_ColumnGrid(component):
    def RunScript(self, nx, ny, bay):
        if not nx or not ny:
            return None
        points = column_grid(nx, ny, bay) if bay else column_grid(nx, ny)
        return [rg.Point3d(p.x, p.y, p.z) for p in points]
