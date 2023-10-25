import math
import compas.geometry as cg

# transform with identity matrix
x = cg.Transformation()
a = cg.Point(1, 0, 0)
b = a.transformed(x)
assert a == b

# translate
t = cg.Translation.from_vector([5, 1, 0])
b = a.transformed(t)
assert b == [6, 1, 0]

# in-place transform
r = cg.Rotation.from_axis_and_angle([0, 0, 1], math.pi)
a.transform(r)
assert repr(a) == repr(cg.Point(-1.0, 0.0, 0.0))

# # rotation from quaternion
# q = cg.Quaternion(0.918958, -0.020197, -0.151477, 0.363544)
# assert q.is_unit

# R = cg.Rotation.from_quaternion(q)
# assert R.quaternion == q
