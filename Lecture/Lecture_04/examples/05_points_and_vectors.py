import compas.geometry as cg

# Point
point = cg.Point(19, 25, 7)

# Vector
vector = cg.Vector(1, 0, 5)

# Access the properties of a point/vector using dot notation
print("point.x: ", point.x)
print("point.y: ", point.y)
print("point.z: ", point.z)

# Access the properties of a point/vector using iteration
print("vector[0]: ", vector[0])
print("vector[1]: ", vector[1])
print("vector[2]: ", vector[2])
