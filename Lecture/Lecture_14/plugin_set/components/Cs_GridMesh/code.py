"""Grasshopper ADAPTER for compas_studio.grid_mesh. Thin on purpose.

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
    raise ImportError(f"{PACKAGE} {VERSION} is not installed; install it with the Package Manager")


_lib = _package_lib()
if _lib not in sys.path:
    sys.path.insert(0, _lib)

# ---------------------------------------------------------------------------
from ghpythonlib.componentbase import executingcomponent as component  # noqa: E402

from compas_studio import grid_mesh  # noqa: E402
from compas_rhino.conversions import mesh_to_rhino  # noqa: E402


class Cs_GridMesh(component):
    def RunScript(self, nx, ny, spacing):
        if not nx or not ny:
            return None
        kwargs = {"spacing": spacing} if spacing is not None else {}
        mesh = grid_mesh(nx, ny, **kwargs)
        return mesh_to_rhino(mesh)
