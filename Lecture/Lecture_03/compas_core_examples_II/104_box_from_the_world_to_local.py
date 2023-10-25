"""Example: Bring a box from the world coordinate system into another coordinate system.
"""
import compas
import compas.geometry as cg

# Box in the world coordinate system
box_frame = cg.Frame([1, 0, 0], [-0.45, 0.1, 0.3], [1, 0, 0])
width, length, height = 1, 1, 1
box = cg.Box(box_frame, width, length, height)

# Frame F representing a coordinate system
F = cg.Frame([2, 2, 2], [0.978, 0.010, -0.210], [0.090, 0.882, 0.463])

# Represent box frame in frame F and construct new box
box_frame_transformed = F.to_world_coordinates(box_frame)
box_transformed = cg.Box(box_frame_transformed, width, length, height)
print("Box frame transformed:", box_transformed.frame)

# Draw!
geometries = [F, box, box_frame, box_transformed, box_frame_transformed]
if compas.is_grasshopper():
    a = geometries
else:
    from compas_view2.app import App
    viewer = App()
    for geometry in geometries:
        viewer.add(geometry)
    viewer.run()
