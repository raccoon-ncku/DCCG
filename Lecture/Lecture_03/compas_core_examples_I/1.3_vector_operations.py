import compas.geometry as cg

# Vectors have a length, and support operations
# such as dot product, cross product, angle calculation,
# unitisation, scaling, etc.

u = cg.Vector(3, 0, 0)
v = cg.Vector(0, 2, 0)

print("u.length: ", u.length)
print("u.dot(v): ", u.dot(v)) # dot product
print("u.cross(v): ", u.cross(v)) # cross product
print("u.angle(v): ", u.angle(v)) # angle between two vectors

u.unitize() # unitisation, i.e. make the vector length = 1
print("after u.unitize(), u.length: ", u.length)