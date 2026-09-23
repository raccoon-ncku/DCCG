"""
Inheritance — a subclass reuses and specialises another class.

The test is "IS-A":
  - A Square IS-A Rectangle — fine, inherit.
  - A Wall is NOT-A kind of Box — it HAS boxes, so it should HOLD a list.
Composition ("has-a") is the right default; reach for inheritance only when
the subclass genuinely is a specialised version of the parent.
"""


class Rectangle:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("a rectangle needs positive dimensions")
        self.width = width
        self.height = height

    def __repr__(self):
        return f"{type(self).__name__}({self.width} × {self.height})"

    @property
    def area(self):
        return self.width * self.height


class Square(Rectangle):
    """A rectangle whose sides are equal."""

    def __init__(self, side):
        # super() calls the parent's method — here, Rectangle.__init__ —
        # so validation (positive dimensions) still runs. Do not duplicate it.
        super().__init__(side, side)


# --- Square gets everything Rectangle has for free ----------------------

s = Square(5)
print(s)                          # Square(5 × 5)     -- via inherited __repr__
print(s.area)                     # 25                -- via inherited @property


# --- isinstance / issubclass --------------------------------------------

print(isinstance(s, Square))      # True
print(isinstance(s, Rectangle))   # True    -- a Square IS-A Rectangle
print(issubclass(Square, Rectangle))  # True


# --- specialising: overriding a method ----------------------------------

class LabelledSquare(Square):
    def __init__(self, side, label):
        super().__init__(side)   # run Square's constructor
        self.label = label

    def __repr__(self):
        # A different string — but if a caller relies on the parent's format
        # this can surprise them. Only override when the parent's behaviour
        # is genuinely wrong for you.
        return f"LabelledSquare({self.label}, {self.width})"


t = LabelledSquare(3, "hero")
print(t)                          # LabelledSquare(hero, 3)
print(t.area)                     # 9


# --- composition — the alternative you reach for MORE often -------------

# A Wall is not a Rectangle; it has one. Storing that as an attribute is
# clearer than inheriting from a class that does not describe the Wall itself.
class Wall:
    def __init__(self, plan, height):
        self.plan = plan          # a Rectangle representing the footprint
        self.height = height

    @property
    def volume(self):
        return self.plan.area * self.height


w = Wall(plan=Rectangle(6, 0.2), height=3)
print(w.volume)                   # 3.6
