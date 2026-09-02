"""Grasshopper ADAPTER for compas_studio.grid_mesh. Thin on purpose."""
# r: compas
# r: compas_studio

from ghpythonlib.componentbase import executingcomponent as component

from compas_studio import grid_mesh
from compas_rhino.conversions import mesh_to_rhino


class Cs_GridMesh(component):
    def RunScript(self, nx, ny, spacing):
        if not nx or not ny:
            return None
        kwargs = {"spacing": spacing} if spacing is not None else {}
        mesh = grid_mesh(nx, ny, **kwargs)
        return mesh_to_rhino(mesh)
