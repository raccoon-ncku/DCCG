"""
Class — a blueprint for creating objects.

The smallest possible example, kept deliberately abstract to name the parts:
class, attribute, method, instance. The next files use a real geometric
class (Rectangle, Vector2D) to make the pattern concrete.
"""


class Rectangle:
    """A rectangle, axis-aligned, defined by its width and height."""

    def __init__(self, width, height):
        """Constructor — runs when you create an instance."""
        self.width = width       # an ATTRIBUTE, stored on this instance
        self.height = height

    def area(self):
        """A METHOD — a function that belongs to the class."""
        return self.width * self.height


# Create an instance. __init__ runs here.
r = Rectangle(3, 4)

# Read an attribute (no parentheses)
print(r.width)                   # 3
print(r.height)                  # 4

# Call a method (parentheses)
print(r.area())                  # 12
