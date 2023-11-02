import compas.geometry as cg

axis, angle = [0.2, 0.4, 0.1], 0.3
R = cg.Rotation.from_axis_and_angle(axis, angle)

# Transform a point
p = cg.Point(1, 1, 1)
t1 = p.transformed(R)
print(t1) # t1 is a new point
print(p) # p is not changed
t2 = p.transform(R)
print(t2) # t2 is none
print(p) # p is changed