import compas
import compas.geometry as cg

# Point, Vector & Plane
point = cg.Point(19, 20, 11)
vector = cg.Vector(0, 3, 1)
plane = cg.Plane(point, vector)

# Frame
origin = cg.Point(19, -20, 11)
xaxis = [1, 0, 0]
yaxis = [0, 1, 0]
frame = cg.Frame(origin, xaxis, yaxis)

geometries = [plane, frame]

if compas.is_grasshopper():
    a = frame # Plane is not defined in GH/Rhino
else:
    from compas_view2.app import App
    viewer = App()
    for geometry in geometries:
        viewer.add(geometry)
    viewer.run()
