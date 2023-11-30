# Create a recursive tree using compas
import random
import compas.geometry as cg
from compas_view2.app import App
viewer = App(show_grid=False)
MAX_DEPTH = 5

def branch(parent_stem, length, depth, angle_deviation=0.9):
    # base case, stop recursion
    if depth > MAX_DEPTH:
        return

    # recursive case, keep going

    # Copy the parent stem's start point and direction
    new_start= parent_stem.end.copy()
    frame = cg.Frame.from_plane(cg.Plane(new_start, parent_stem.direction))

    # Rotate the direction by a random amount
    rotation_1 = cg.Rotation.from_axis_and_angle(frame.xaxis,
                                               random.uniform(-angle_deviation, angle_deviation))
    rotation_2 = cg.Rotation.from_axis_and_angle(frame.zaxis,
                                               random.uniform(-angle_deviation, angle_deviation))
    vector = parent_stem.direction.transformed(rotation_1 * rotation_2)
    
    # Scale the direction by the length
    vector.scale(length)

    # Create a new end point and stem
    end = new_start.transformed(cg.Translation.from_vector(vector))
    new_stem = cg.Line(new_start, end)

    # Draw the stem
    viewer.add(new_stem, linecolor=(0, 0, 0), linewidth=2)

    # Recurse
    branch(new_stem, length * 0.7, depth + 1)
    branch(new_stem, length * 0.7, depth + 1)

init_stem = cg.Line(cg.Point(0, 0, 0), cg.Point(0, 0, 5))
viewer.add(init_stem, linecolor=(0, 0, 0), linewidth=2)
branch(init_stem, 5, 0)
viewer.run()