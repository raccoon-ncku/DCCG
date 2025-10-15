import compas.geometry as cg

# Frame is created by a point and two vectors
frame = cg.Frame(
    cg.Point(15, 24, 3),
    cg.Vector(1, 0, 0),
    cg.Vector(0, 1, 0)
)

# The base point and the three axes of the frame
# can be accessed by their respective properties: 
#  point, xaxis, yaxis, and zaxis,
print("frame.point: ", frame.point)
print("type(frame.point): ", type(frame.point))
print("frame.point.x: ", frame.point.x)
print("frame.xaxis: ", frame.xaxis)
print("frame.xaxis.x: ", frame.xaxis.x)