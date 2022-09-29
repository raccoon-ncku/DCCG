"""Example: 'point in frame'

The simple example above shows how to use a frame as a coordinate system:
Starting from a point `P` in the local (user-defined, relative) coordinate
system of frame `F`, i.e. its position is relative to the origin and orientation
of `F`, we want to get the position `P_` of `P` in the global (world, absolute)
coordinate system.
"""
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import allclose
import compas

point = Point(2.00, 2.00, 2.00)
xaxis = Vector(0.9767, 0.0010, -0.214)
yaxis = Vector(0.1002, 0.8818, 0.4609)

F = Frame(point, xaxis, yaxis)  # coordinate system F
P = Point(3., 3., 3.)  # point in F (local coordinates)

P_ = F.to_world_coordinates(P)  # point in global (world) coordinates
print("The point's world coordinates: {}".format(P_))

P2 = F.to_local_coordinates(P_)
print("The point's local coordinates: {}".format(P2))  # should equal P
print("Are the two points equal? {}".format(allclose(P2, P)))

# Draw!
geometries = [F, Point(*P_)]

if compas.is_grasshopper():
    a = geometries
else:
    from compas_view2.app import App
    viewer = App()
    for geometry in geometries:
        viewer.add(geometry)
    viewer.run()