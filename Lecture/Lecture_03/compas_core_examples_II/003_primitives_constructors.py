import compas.geometry as cg

a = cg.Vector(1, 0, 0)
b = cg.Vector.from_start_end([1, 0, 0], [2, 0, 0])
assert a == b

a = cg.Plane([0, 0, 0], [0, 0, 1])
b = cg.Plane.from_three_points([0, 0, 0], [1, 0, 0], [0, 1, 0])
assert a == b

a = cg.Frame([0, 0, 0], [3, 0, 0], [0, 2, 0])
b = cg.Frame.from_points([0, 0, 0], [5, 0, 0], [1, 2, 0])
assert a == b
