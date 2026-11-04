import compas.geometry as cg

point_a = cg.Point(19, 25, 7)
point_b = cg.Point(2, 3, 5)

# Points and vectors support basic arithmetic operations 
# such as addition, subtraction, multiplication, and division.
print("point_a + point_b: ", point_a + point_b)
print("point_a - point_b: ", point_a - point_b) #subtraction of two points returns a vector
print("point_a * 2: ", point_a * 2)
print("point_a / 2: ", point_a / 2)