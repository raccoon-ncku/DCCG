"""
Grasshopper ADAPTER for compas_studio.running_bond_wall.

This file is the whole point of the course, in miniature. Look how little it
does: it takes the Grasshopper inputs, calls ONE function from the tested
core, converts the result to Rhino geometry, and returns it. There is no
geometry logic here to get wrong -- that logic lives in compas_studio.wall,
where pytest has already checked it (headlessly, with no Rhino in sight).

The componentizer turns this folder into Cs_RunningBondWall.ghuser using GitHub
Actions, on a Windows runner, with Rhino installed nowhere. Keep adapters this
thin: an adapter you can read in ten seconds is an adapter you do not need to
test.
"""
# r: compas
# r: compas_studio

from ghpythonlib.componentbase import executingcomponent as component

from compas_studio import running_bond_wall
from compas_rhino.conversions import box_to_rhino


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
