import math
import compas.geometry as cg
from compas_view2.app import App
from compas_view2.objects import Collection

viewer = App(enable_sidebar=True, show_grid=False)

MAX_DEPTH = 5
theta = 90

new_branches = []

def branch(parent_stem, length, depth, theta):
    # base case, stop recursion
    if depth > MAX_DEPTH:
        return

    pass

# initial stem
init_stem = cg.Line(cg.Point(0, 0, 0), cg.Point(0, 5, 0))
viewer.add(init_stem, linecolor=(0, 0, 0), linewidth=2)

# recursive branch
branch(init_stem, 5, 0, theta)

# add branches to viewer
viewer_objs = []
for _branch in new_branches:
    viewer_objs.append(viewer.add(_branch, linecolor=(0, 0, 0), linewidth=2))

@viewer.slider(title="THETA", value=30, minval=1, maxval=180, step=1)
def slide(value):
    global new_branches # reset branches
    new_branches = []
    branch(init_stem, 5, 0, value)
    for i, new_branch in enumerate(new_branches):
        viewer_objs[i]._data = new_branch
        viewer_objs[i].update()

viewer.run()