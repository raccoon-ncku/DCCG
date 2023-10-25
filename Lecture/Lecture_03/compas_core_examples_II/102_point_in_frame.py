"""Example: 'point in frame'

The simple example above shows how to use a frame as a coordinate system:
Starting from a point `P` in the local (user-defined, relative) coordinate
system of frame `F`, i.e. its position is relative to the origin and orientation
of `F`, we want to get the position `P_` of `P` in the global (world, absolute)
coordinate system.
"""
import compas
import compas.geometry as cg

point = cg.Point(2.00, 2.00, 2.00)
xaxis = cg.Vector(0.9767, 0.0010, -0.214)
yaxis = cg.Vector(0.1002, 0.8818, 0.4609)

F = cg.Frame(point, xaxis, yaxis)  # coordinate system F
P = cg.Point(3., 3., 3.)  # point in F (local coordinates)

P_ = F.to_world_coordinates(P)  # point in global (world) coordinates
print("The point's world coordinates: {}".format(P_))

P2 = F.to_local_coordinates(P_)
print("The point's local coordinates: {}".format(P2))  # should equal P
print("Are the two points equal? {}".format(cg.allclose(P2, P)))

# Draw!
if compas.is_grasshopper():
    a = [F, cg.Point(*P_)]
else:
    from compas_view2.app import App
    viewer = App()
    viewer.add(F)
    viewer.add(cg.Point(*P_))
    viewer.run()
