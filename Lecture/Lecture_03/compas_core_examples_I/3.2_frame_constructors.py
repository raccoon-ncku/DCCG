import compas.geometry as cg

# Frame autocorrects axes to be orthonormal
F = cg.Frame(cg.Point(1, 0, 0), cg.Vector(-0.45, 0.1, 0.3), cg.Vector(1, 0, 0))

# Frames can also be constructed from simple lists or tuples containing
# the XYZ coordinates of the base point and the two input vectors.
F = cg.Frame([1, 0, 0], [-0.45, 0.1, 0.3], [1, 0, 0])

# Frames can also be constructed from three points.
F = cg.Frame.from_points([1, 1, 1], [2, 3, 6], [6, 3, 0])

# Frames can also be constructed to
# match specific planes of the world coordinate system.
F = cg.Frame.worldXY()