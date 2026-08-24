# Week 07 — Object-oriented programming  🚫 *no class this week*

> **2026.10.21 — I am at a conference. This week runs without me.**
>
> Everything you need is on this page. Work at your own pace, check yourself
> with `uv run check.py 07`, and push your work by Sunday so I can see where
> everyone got to.

## How to run a week without an instructor

This is a rehearsal, not a gap. The skill being trained is the one you will
need for the rest of your career: **learning something new, from written
material and a machine that answers questions, and knowing whether you
actually got it.**

A workable routine:

1. Read §1–§5 below and run the examples as you go. ~60 minutes.
2. Start the checkpoints. Get stuck. **Stay stuck for ten minutes** before
   asking anything — that is where the learning happens.
3. Then ask your AI assistant, but ask it the *right* question:
   - ✅ "Explain what `self` means in this method, as if I have used
     functions but never classes."
   - ✅ "Why does my `__repr__` not show when I print a list of these?"
   - ❌ "Write me a Vector2D class." *(You will pass the checkpoint and learn
     nothing, and Week 11 will be much harder.)*
4. The checkpoints are your marker. Nobody is watching; the only person you
   can cheat is the one who has to build a final project in December.
5. Stuck for real? Open an issue on the course repo, or email me — I read mail
   at the conference, just slowly.

---

## 1. Why classes

You can already model a wall with a function returning boxes. So why this?

Because some things have **state and behaviour that belong together**. Consider
a `Walker` that wanders through space leaving spheres: it has a position, and
it can step. With functions you would pass the position in and out of every
call, by hand, forever:

```python
position, radius = step(position, radius)
position, radius = step(position, radius)
```

With a class, the thing remembers what it is:

```python
walker = Walker(start=(0, 0, 1), radius=1.0)
walker.walk()
walker.walk()
```

**Use a class when data and the operations on it are inseparable.** Use a plain
function when they are not. A class that is only a bag of functions with no
state is a module wearing a costume.

## 2. Defining a class

```python
class Rectangle:
    """A rectangle, axis-aligned, defined by its width and height."""

    def __init__(self, width, height):
        """The constructor -- runs when you create an instance."""
        self.width = width          # an ATTRIBUTE, stored on this instance
        self.height = height

    def area(self):
        """A METHOD -- a function that belongs to the class."""
        return self.width * self.height


r = Rectangle(3, 4)      # __init__ runs here
r.width                  # 3
r.area()                 # 12
```

### `self`

Every method's first parameter is `self`: the particular instance it was
called on. You never pass it — `r.area()` becomes `Rectangle.area(r)`
automatically.

Forgetting `self` is the beginner error of this week:

```python
def area(self):
    return width * height        # NameError -- `width` is not a bare name
    return self.width * self.height   # correct
```

📄 `class_examples/8.1_class.py`, `8.2.1_class_constructor.py`

## 3. Dunder methods

Methods with `__double_underscores__` hook into Python's built-in syntax.
This is what makes a class feel like a real type rather than a struct.

```python
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        """What you see when you print it. Make it useful."""
        return f"Vector2D({self.x}, {self.y})"

    def __add__(self, other):
        """Makes `a + b` work."""
        return Vector2D(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        """Makes `a == b` compare values instead of identity."""
        return self.x == other.x and self.y == other.y
```

Without `__repr__`, printing gives you
`<Vector2D object at 0x104f8a>` — useless when debugging a list of 200 of them.
**Write `__repr__` on every class you make.** It costs one line and it is the
difference between a readable and an unreadable error message.

📄 `class_examples/8.2.2_str_methods.py`, `8.2.3_arithmetic_operators.py`

## 4. Properties

A **property** is a method you access without parentheses — for values that
are *derived* rather than stored.

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height


r = Rectangle(3, 4)
r.area          # 12   -- no parentheses
r.width = 10
r.area          # 40   -- recomputed, never stale
```

Why not just store `self.area = width * height` in `__init__`? Because then
changing `width` leaves `area` silently wrong. **Derive, do not duplicate.**
Two copies of one fact will disagree eventually, and the moment they do is
never the moment you are looking.

📄 `class_examples/8.3.1_class_attribute.py`, `8.3.3_property.py`

### Validating in the constructor

```python
def __init__(self, width, height):
    if width <= 0 or height <= 0:
        raise ValueError("a rectangle needs positive dimensions")
    self.width = width
    self.height = height
```

Refuse to build a nonsensical object at all. An object that cannot exist in an
invalid state is one you never have to defend against later.

### Class methods — alternative constructors

```python
@classmethod
def square(cls, side):
    return cls(side, side)

r = Rectangle.square(5)
```

📄 `class_examples/8.3.4_class_method.py`

## 5. Inheritance

A subclass reuses and specialises another class.

```python
class Square(Rectangle):
    """A rectangle whose sides are equal."""

    def __init__(self, side):
        super().__init__(side, side)      # run Rectangle's constructor
```

`Square` gets `area` for free. `isinstance(Square(2), Rectangle)` is `True`.

Inheritance is easy to overuse. The test is **"is-a"**: a square *is a*
rectangle, so this is fine. A wall is *not a* kind of box — it *has* boxes, so
it should hold a list, not inherit. Composition ("has-a") is the right default;
reach for inheritance when the subclass genuinely is a specialised version of
the parent.

📄 `class_examples/8.4.1_inheritance.py`

## 6. Classes and the Week 06 architecture

A class can be pure. `Wall` in checkpoint 4 holds parameters, validates them,
derives values, and produces geometry on request — and imports no viewer, no
files, no Rhino. It belongs in the **core** layer exactly as the function did.

Objects do not change the architecture. They organise what is inside a layer.

## 7. Optional: agent-based models

`abm_examples/` contains ants and drones — many simple objects, each following
local rules, producing collective behaviour. It is the most natural use of
classes in design computation, and a strong final-project direction. Read it if
it appeals; nothing this week depends on it.

📄 `abm_examples/ants/`, `abm_examples/drone/`

---

## Checkpoints

```bash
uv run check.py 07
```

| # | Task | Exercises |
| - | ---- | --------- |
| 1 | `Vector2D` | `__init__`, `__repr__`, `__add__`, `__eq__`, a property |
| 2 | `Rectangle` | properties, validation, a method taking another object |
| 3 | `Square(Rectangle)` | inheritance and `super()` |
| 4 | `Wall` | a class in the core layer — and it stays pure |

## Exercises

📝 [Vector2D and Rectangle](/Exercise/Lecture_08/README.md) — the same ground,
worked differently.
📝 [Re-write to OOP](/Exercise/2_re-write_to_oop/README.md) — take the random
walker and turn it into a class. Good practice for checkpoint 4.

## Self-test

1. What is `self`, and why do you never pass it in?
2. When should a value be a `@property` rather than set in `__init__`?
3. Why write `__repr__` on every class?
4. A `Wall` contains boxes. Should `Wall` inherit from `Box`? Why not?
5. What does `super().__init__(...)` do?

## Before Sunday

```bash
uv run check.py 07     # all green?
git add -A && git commit -m "Week 07: OOP checkpoints"
git push
```

Bring one question to Week 09 — we open with a debrief and a peer code review
of these two self-paced weeks.
