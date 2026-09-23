"""
Dunder methods for ARITHMETIC.

Define __add__ and Python's `+` works on your instances. Same for __sub__,
__mul__, __eq__, __neg__, etc. This is what turns a data-holder into a
type that composes naturally.
"""


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    # Makes `a + b` work
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    # Makes `a - b` work
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    # Makes `k * v` work — scalar multiplication
    def __mul__(self, k):
        return Vector2D(self.x * k, self.y * k)

    # Makes `-v` work
    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    # Makes `a == b` compare VALUES instead of identity
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


a = Vector2D(1, 2)
b = Vector2D(3, 4)

print(a + b)                      # Vector2D(4, 6)
print(b - a)                      # Vector2D(2, 2)
print(a * 3)                      # Vector2D(3, 6)
print(-a)                         # Vector2D(-1, -2)

# Value equality — two vectors with the same coords are "equal" even
# though they are different objects.
print(a == Vector2D(1, 2))        # True
print(a is Vector2D(1, 2))        # False  -- `is` compares identity
