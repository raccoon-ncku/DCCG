"""
The constructor (__init__) and the meaning of `self`.

Every method's first parameter is `self` — the particular instance the
method was called on. You never pass it yourself. `r.area()` becomes
`Rectangle.area(r)` automatically.
"""


class Rectangle:
    """A rectangle defined by its width and height."""

    def __init__(self, width, height):
        """Runs when you write `Rectangle(3, 4)`."""
        self.width = width
        self.height = height

    def area(self):
        # `self` refers to THIS particular rectangle.
        # Forgetting `self.` here is the classic beginner error:
        #   return width * height          # NameError -- bare name
        return self.width * self.height

    def scale(self, factor):
        """Grow (or shrink) this rectangle in place, returning self for chaining."""
        self.width *= factor
        self.height *= factor
        return self


# --- two instances, independent state ------------------------------------

small = Rectangle(1, 2)
big = Rectangle(5, 8)

print(small.area())               # 2
print(big.area())                 # 40

# Each instance has its OWN width and height. Changing one does not touch the other.
small.scale(3)
print(small.area())               # 18   (small changed)
print(big.area())                 # 40   (big unaffected)


# --- forgetting `self.` — the error message you will see ----------------

class Broken:
    def __init__(self, x):
        self.x = x

    def show(self):
        try:
            return x                # bare `x`, no self
        except NameError as e:
            return f"NameError: {e}"

print(Broken(7).show())
