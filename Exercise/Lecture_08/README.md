# Class
1. Create a `Vector2D` class:
   - It has two attributes: `x` and `y`.
   - When printing a vector, it should be printed as `Vector2D(x, y)`.
   - When `x` and `y` are not given, they should be set to `0`.
   - When adding two vectors, the `+` operator should return **a new vector** whose `x` and `y` are the sum of the two vectors.
   - It has a method named `dot` that returns the dot product of the vector.
   - It has a class attribute named `name` that is set to `Vector2D`.
   - Create two vectors and print their dot product and addition result, also print the class attribute `name`.
2. Create a `Rectangle` class:
   - It has two attributes: `width` and `height`.
   - It has a method named `area` that returns the area of the rectangle.
   - It has a method named `perimeter` that returns the perimeter of the rectangle. 
   - `area` and `perimeter` should be properties, i.e. you can access them without using `()`, but you cannot assign values to them.
   - It has a class method named `from_two_points` that returns a rectangle given two points.
   - Create a rectangle and print its area and perimeter with default constructor.
   - Create a rectangle and print its area and perimeter with `from_two_points` method.

# Agent-Based Modeling
Using the given code `drone.py` and `dynamic_view_drone.py`, create a drone agent that will be attracted to a given point.