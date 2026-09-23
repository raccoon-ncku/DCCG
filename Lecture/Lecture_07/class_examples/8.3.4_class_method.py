"""
@classmethod — an alternative constructor.

Sometimes there is more than one natural way to make an instance. Rather
than jamming every case into __init__ with confusing defaults, define a
@classmethod that takes different inputs and returns a fresh instance.
"""


class Rectangle:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("a rectangle needs positive dimensions")
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Rectangle({self.width} × {self.height})"

    # --- alternative constructors ------------------------------------

    @classmethod
    def square(cls, side):
        """Make a square — one side length, both dimensions equal."""
        # `cls` is the class itself. Using cls(...) instead of Rectangle(...)
        # means this also works for subclasses (see 8.4.1_inheritance.py).
        return cls(side, side)

    @classmethod
    def from_diagonal(cls, diagonal, aspect):
        """Make a rectangle from its diagonal length and width/height ratio."""
        # aspect = width / height, so:
        #   width  = height * aspect
        #   diag^2 = width^2 + height^2 = height^2 * (aspect^2 + 1)
        height = (diagonal ** 2 / (aspect ** 2 + 1)) ** 0.5
        width = height * aspect
        return cls(width, height)


# --- three ways to construct a Rectangle --------------------------------

a = Rectangle(3, 4)                       # the direct constructor
b = Rectangle.square(5)                   # via @classmethod
c = Rectangle.from_diagonal(5, aspect=4/3)  # 3-4-5 triangle

print(a)                                  # Rectangle(3 × 4)
print(b)                                  # Rectangle(5 × 5)
print(c)                                  # Rectangle(4.0 × 3.0)


# --- @staticmethod: no `self`, no `cls` ---------------------------------

# A plain function that happens to be inside the class. Use it when the
# logic BELONGS to the class conceptually but does not need any of its state.

class Geometry:
    @staticmethod
    def clamp(value, low, high):
        return max(low, min(value, high))


print(Geometry.clamp(15, 0, 10))          # 10
print(Geometry.clamp(-3, 0, 10))          # 0
