"""Grasshopper ADAPTER for compas_studio.straight_staircase. Thin on purpose."""
# r: compas
# r: compas_studio

from ghpythonlib.componentbase import executingcomponent as component

from compas_studio import straight_staircase
from compas_rhino.conversions import box_to_rhino


class Cs_Staircase(component):
    def RunScript(self, n_steps, rise, tread, width):
        if not n_steps:
            return None
        kwargs = {}
        if rise is not None:
            kwargs["rise"] = rise
        if tread is not None:
            kwargs["tread"] = tread
        if width is not None:
            kwargs["width"] = width
        steps = [box_to_rhino(b) for b in straight_staircase(n_steps, **kwargs)]
        return steps
