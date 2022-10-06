import compas
import compas.geometry as cg

# Point
point = cg.Point(19, 25, 7)

# Polyline
p1 = [0, 0, 0]
p2 = [1, 0, 0]
p3 = [1, 1, 0]
p4 = [0, 0, 0]
polyline = cg.Polyline([p1, p2, p3, p4])

# Polygon
polygon = cg.Polygon([p1, p2, p3])

geometries = [point, polyline, polygon]


# Visualization
if compas.is_grasshopper():
    a = geometries
else:
    from compas_view2.app import App
    viewer = App()
    for geometry in geometries:
        viewer.add(geometry)
    viewer.run()
