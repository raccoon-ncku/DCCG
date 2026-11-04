import compas.geometry as cg

# create a transformation
# This is the identity transformation
T = cg.Transformation()

# The transformation is a 4x4 matrix
print(T)

# Transformations can be applied to all geometry objects
# through the Geometry.transform() method.
point = cg.Point(1, 2, 3)
point.transform(T)
print(point) # == (1, 2, 3), as expected