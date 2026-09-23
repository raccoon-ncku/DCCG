"""
Dunder methods for STRING REPRESENTATION.

- __repr__ is what you see in the REPL, in a list, in a traceback.
  Write it on EVERY class you make. It costs one line and is the difference
  between a readable and an unreadable error message.

- __str__ is what print() shows. If you don't define it, print() falls back
  to __repr__ — which is usually what you want.
"""


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        # A useful __repr__ shows enough that a reader could reconstruct
        # the object. Convention: looks like a Python expression.
        return f"Vector2D({self.x}, {self.y})"


v = Vector2D(3, 4)

# Without __repr__ we would see something useless like
#   <Vector2D object at 0x104f8a>
# Try commenting the __repr__ out and re-running.
print(v)                          # Vector2D(3, 4)

# In a list, __repr__ is what shows for each element:
print([Vector2D(0, 0), Vector2D(1, 0), Vector2D(0, 1)])


# --- __str__ when you want a different HUMAN string ---------------------

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Rectangle({self.width}, {self.height})"

    def __str__(self):
        return f"a {self.width}×{self.height} rectangle"


r = Rectangle(3, 4)
print(str(r))                     # 'a 3×4 rectangle'   (uses __str__)
print(repr(r))                    # 'Rectangle(3, 4)'   (uses __repr__)
print(f"{r}")                     # 'a 3×4 rectangle'   (f-string uses __str__)
print(f"{r!r}")                   # 'Rectangle(3, 4)'   (!r forces __repr__)
