import compas.geometry as cg

# Point
assert [0, 5, 1] == cg.Point(0, 5, 1)

# Vector
assert [0, 0, 1] == cg.Vector(0, 0, 1)

# Plane
point = [0, 0, 0]
vector = [1, 0, 0]
assert (point, vector) == cg.Plane(point, vector)

# Frame
point = [5, 0, 0]
xaxis = [1, 0, 0]
yaxis = [0, 1, 0]
assert (point, xaxis, yaxis) == cg.Frame(point, xaxis, yaxis)

# Polyline
p1 = [0, 0, 0]
p2 = [1, 0, 0]
p3 = [1, 1, 0]
p4 = [0, 0, 0]
assert [p1, p2, p3, p4] == cg.Polyline([p1, p2, p3, p4])

# Polygon
assert [p1, p2, p3] == cg.Polygon([p1, p2, p3])
