# Create a recursive tree using compas
import random
import compas.geometry as cg
from compas_viewer import Viewer
viewer = App(show_grid=False)
MAX_DEPTH = 4

def branch(parent_stem, length, depth, angle_deviation=0.5):
    # base case, stop recursion
    random_stop = random.random()

    if random_stop < 0.3:
        return
    if depth > MAX_DEPTH:
        sphere = cg.Sphere(parent_stem.end, 0.3)
        viewer.scene.add(sphere, facecolor=(1, 0, 0))
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
    viewer.scene.add(new_stem, linecolor=(0, 0, 0), linewidth=5-depth)

    # Recurse
    branch_count = random.randint(2, 4)
    for i in range(branch_count):
        branch(new_stem, length * 0.9, depth + 1)

init_stem = cg.Line(cg.Point(0, 0, 0), cg.Point(0, 0, 5))
viewer.scene.add(init_stem, linecolor=(0, 0, 0), linewidth=5)
branch(init_stem, 5, 0)
viewer.show()