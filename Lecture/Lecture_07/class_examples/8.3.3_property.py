"""
@property — a method you access WITHOUT parentheses, for values that are
DERIVED rather than stored.

The rule: derive, do not duplicate. Two copies of one fact will disagree
eventually, and the moment they do is never the moment you are looking.
"""


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        # No self.area stored anywhere. Recomputed each read.
        return self.width * self.height

    @property
    def perimeter(self):
        return 2 * (self.width + self.height)


r = Rectangle(3, 4)

# Note: no parentheses. That is the whole point of @property.
print(r.area)                    # 12
print(r.perimeter)               # 14

# Change an input; the derived value is up to date automatically.
r.width = 10
print(r.area)                    # 40   -- recomputed, never stale


# --- validation via a setter: refuse a bad assignment -------------------

class Positive:
    """A number that refuses to be negative."""

    def __init__(self, value):
        self.value = value       # goes through the setter below

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new):
        if new < 0:
            raise ValueError(f"must be >= 0, got {new}")
        self._value = new


p = Positive(5)
print(p.value)                   # 5
p.value = 12                     # fine
try:
    p.value = -3                 # rejected
except ValueError as e:
    print("rejected:", e)


# The alternative is to write get_x() / set_x() everywhere, which every
# other language forces you to do. @property lets you START with a plain
# attribute and add validation LATER without changing any caller.
