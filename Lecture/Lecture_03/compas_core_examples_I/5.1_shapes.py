import compas.geometry as cg
from compas_view2.app import App

# Box is created from a frame and xsize, ysize, zsize
box = cg.Box(cg.Frame.worldXY(), 10, 1, 4)

# Sphere is created from a point and radius
sphere = cg.Sphere([10, 0, 0], 4)

# Cylinder is created from a circle and height
plane = cg.Plane([20, 0, 0], [0, 0, 1])
circle = cg.Circle(plane, 5)
cylinder = cg.Cylinder(circle, height=4)

geometries = [box, sphere, cylinder]

# visualize
viewer = App()
for geometry in geometries:
    viewer.add(geometry)
viewer.run()
