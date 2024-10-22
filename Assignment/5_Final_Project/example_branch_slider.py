import math
import compas.geometry as cg
from compas_viewer import Viewer
from compas_view2.objects import Collection

viewer = App(enable_sidebar=True, show_grid=False)

MAX_DEPTH = 8
theta = 90

new_branches = []

def branch(parent_stem, length, depth, theta):
    # base case, stop recursion
    if depth > MAX_DEPTH:
        return

    # create new stem
    new_start = parent_stem.end.copy()
    frame = cg.Frame(
        new_start,
        cg.Vector.Zaxis().cross(parent_stem.direction),
        parent_stem.direction
    )

    rotation_1 = cg.Rotation.from_axis_and_angle(
        frame.zaxis, math.radians(theta)
    )
    rotation_2 = cg.Rotation.from_axis_and_angle(
        frame.zaxis, math.radians(-theta)
    )
    tranlation = cg.Translation.from_vector(
        cg.Vector(*new_start))
    new_stem = cg.Line(
        cg.Point(0, 0, 0),
        cg.Point(0, 0, 0) + frame.yaxis * length
    )
    new_stem_1 = new_stem.transformed(
        tranlation * rotation_1)
    new_stem_2 = new_stem.transformed(
        tranlation * rotation_2)
    new_branches.append(new_stem_1)
    new_branches.append(new_stem_2)
    # Recurse
    branch(new_stem_1, length * 0.7, depth + 1, theta)
    branch(new_stem_2, length * 0.7, depth + 1, theta)


# initial stem
init_stem = cg.Line(cg.Point(0, 0, 0), cg.Point(0, 5, 0))
viewer.scene.add(init_stem, linecolor=(0, 0, 0), linewidth=2)

# recursive branch
branch(init_stem, 5, 0, theta)

# add branches to viewer
viewer_objs = []
for _branch in new_branches:
    viewer_objs.append(viewer.scene.add(_branch, linecolor=(0, 0, 0), linewidth=2))

@viewer.slider(title="THETA", value=30, minval=1, maxval=180, step=1)
def slide(value):
    global new_branches # reset branches
    new_branches = []
    branch(init_stem, 5, 0, value)
    for i, new_branch in enumerate(new_branches):
        viewer_objs[i]._data = new_branch
        viewer_objs[i].update()

viewer.show()