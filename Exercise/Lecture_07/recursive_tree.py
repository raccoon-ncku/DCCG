# Create a recursive tree using compas
import random
import compas.geometry as cg
from compas_view2.app import App
viewer = App(show_grid=False)
MAX_DEPTH = 5

def branch(parent_stem, length, depth, max_depth, angle_deviation=0.9):
    if depth > max_depth:
        return
    new_start= parent_stem.end.copy()
    frame = cg.Frame.from_plane(cg.Plane(new_start, parent_stem.direction))
    rotation = cg.Rotation.from_axis_and_angle(frame.xaxis,
                                               random.uniform(-angle_deviation, angle_deviation))
    vector = parent_stem.direction.transformed(rotation)
    vector.scale(length)
    end = new_start.transformed(cg.Translation.from_vector(vector))
    new_stem = cg.Line(new_start, end)
    viewer.add(new_stem, linecolor=(0, 0, 0), linewidth=2)
    branch(new_stem, length * 0.7, depth + 1, max_depth)
    branch(new_stem, length * 0.7, depth + 1, max_depth)

init_stem = cg.Line(cg.Point(0, 0, 0), cg.Point(0, 0, 5))
viewer.add(init_stem, linecolor=(0, 0, 0), linewidth=2)
branch(init_stem, 5, 0, MAX_DEPTH)
viewer.run()