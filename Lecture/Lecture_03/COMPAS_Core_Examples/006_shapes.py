import compas
import compas.geometry as cg

# Box
# xsize, ysize, zsize
b1 = cg.Box(cg.Frame.worldXY(), 10, 1, 4)

# width=xsize, height=zsize, depth=ysize
b2 = cg.Box.from_width_height_depth(10, 4, 1)
assert str(b1) == str(b2)
print(b1)

# Sphere
s1 = cg.Sphere([10, 0, 0], 4)
print(s1)

# Cylinder
plane = cg.Plane([20, 0, 0], [0, 0, 1])
circle = cg.Circle(plane, 5)
c1 = cg.Cylinder(circle, height=4)
print(c1)

# Draw!
geometries = [s1, c1]

if compas.is_grasshopper():
    a = geometries
else:
    from compas_view2.app import App
    viewer = App()
    for geometry in geometries:
        viewer.add(geometry)
    viewer.run()
