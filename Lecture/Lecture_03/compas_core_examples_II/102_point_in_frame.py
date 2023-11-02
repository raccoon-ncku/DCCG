"""Example: 'point in frame'

The simple example above shows how to use a frame as a coordinate system:
Starting from a point `P` in the local (user-defined, relative) coordinate
system of frame `F`, i.e. its position is relative to the origin and orientation
of `F`, we want to get the position `P_` of `P` in the global (world, absolute)
coordinate system.
"""
import compas.geometry as cg
from compas_view2.app import App

point = cg.Point(2.00, 2.00, 2.00)
xaxis = cg.Vector(0.9767, 0.0010, -0.214)
yaxis = cg.Vector(0.1002, 0.8818, 0.4609)

F = cg.Frame(point, xaxis, yaxis)  # coordinate system F

# Imagine that we have a point P in the local coordinate system of F.
# Its coordinates are relative to the origin and orientation of F.
# Say, P is at (3, 3, 3) in F's local coordinate system.
P1 = F.to_world_coordinates(cg.Point(1, 2, 3))
print("The point's world coordinates: {}".format(P1))

P2 = F.to_local_coordinates(P1)
print("The point's local coordinates: {}".format(P2))

# Visualisation
viewer = App()
viewer.add(F)
viewer.add(cg.Point(*P1))


# For visualisation purposes, we draw a Box.
b = cg.Box.from_diagonal([[0, 0, 0], [1, 2, 3]])
b.transform(cg.Transformation.from_frame(F))
viewer.add(b,opacity=0.2)


viewer.run()
