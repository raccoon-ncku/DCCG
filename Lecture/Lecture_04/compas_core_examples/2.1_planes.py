import compas.geometry as cg

# Plane is created by a point and a normal vector
plane = cg.Plane(cg.Point(15, 24, 3), cg.Vector(1, 0, 0))

# Access the properties of a plane using dot notation
print("plane.point: ", plane.point)
print("plane.point.x: ", plane.point.x)
print("plane.normal: ", plane.normal)
print("plane.normal.x: ", plane.normal.x)