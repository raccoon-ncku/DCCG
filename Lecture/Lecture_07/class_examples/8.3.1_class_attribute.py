"""
Class attributes vs instance attributes.

- INSTANCE attributes belong to one particular object. Set with `self.foo`
  in __init__. Different for every instance.

- CLASS attributes belong to the class itself. Every instance shares one.
  Useful for defaults, counters, and constants that describe the type.
"""


class Rectangle:
    # A class attribute — shared by every Rectangle
    unit = "m"

    def __init__(self, width, height):
        # Instance attributes — one per Rectangle
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Rectangle({self.width}{self.unit} × {self.height}{self.unit})"


small = Rectangle(1, 2)
big = Rectangle(5, 8)

print(small)                                # Rectangle(1m × 2m)
print(big)                                  # Rectangle(5m × 8m)

# Read the class attribute either way
print(f"small.unit  = {small.unit}")        # from an instance
print(f"Rectangle.unit = {Rectangle.unit}") # from the class


# --- change on the CLASS: everyone sees the new value -------------------

Rectangle.unit = "cm"
print(small)                                # Rectangle(1cm × 2cm)
print(big)                                  # Rectangle(5cm × 8cm)


# --- change on ONE instance: it shadows the class attribute --------------

# Assigning `small.unit` creates an INSTANCE attribute that hides the class one.
# Only `small` is affected; `big` keeps reading the class attribute.
small.unit = "mm"
print(small)                                # Rectangle(1mm × 2mm)
print(big)                                  # Rectangle(5cm × 8cm)


# --- a common trap: mutable class attributes -----------------------------

# If the class attribute is a LIST (or dict, or set) and you mutate it, every
# instance sees the change — because there is only one list. This is a
# frequent bug source and one of the reasons defaults live in __init__.
class Bad:
    tags = []                # shared list!

    def add(self, tag):
        self.tags.append(tag)

a, b = Bad(), Bad()
a.add("first")
print(b.tags)                # ['first'] -- oh
