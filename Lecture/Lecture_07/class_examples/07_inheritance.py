"""Inheritance: a family of classes that answer the same question in their own way.

    uv run Lecture/Lecture_07/class_examples/07_inheritance.py

Two beams meet at a square corner. How much timber does each one need beyond
its centreline? It depends on the joint, so each joint class answers for itself.
"""


class Beam:
    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width


class Joint:
    """What every joint has in common. It does not know how to cut anything."""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def other(self, beam):
        return self.b if beam is self.a else self.a

    def allowance(self, beam):
        raise NotImplementedError(f"{type(self).__name__} must say how much timber it needs")

    def blank(self, beam):
        """Written once, here. It calls whichever allowance() this object has."""
        return beam.length + self.allowance(beam)


class ButtJoint(Joint):
    """a stops at the face of b; b runs on past the corner."""

    def allowance(self, beam):
        half_of_other = self.other(beam).width / 2
        return -half_of_other if beam is self.a else half_of_other


class MiterJoint(Joint):
    """Both are cut at 45 degrees, so both need timber up to the outer corner."""

    def allowance(self, beam):
        return self.other(beam).width / 2


class LabelledButt(ButtJoint):
    """super() runs the parent's version, then adds to it."""

    def __init__(self, a, b, label):
        super().__init__(a, b)
        self.label = label


post = Beam("post", 2400, 100)
plate = Beam("plate", 3600, 100)

# The loop does not care which class it holds. That is polymorphism.
for joint in (ButtJoint(post, plate), MiterJoint(post, plate)):
    print(type(joint).__name__, {beam.name: joint.blank(beam) for beam in (joint.a, joint.b)})
# ButtJoint {'post': 2350.0, 'plate': 3650.0}
# MiterJoint {'post': 2450.0, 'plate': 3650.0}

print(isinstance(ButtJoint(post, plate), Joint))                # True: a butt joint is a joint
print([c.__name__ for c in LabelledButt.__mro__])               # the order Python looks for a method

# Classes are values, so a rule can be a dictionary (Week 06 §11).
RULE = {"corner": MiterJoint, "end_on_side": ButtJoint}
print(RULE["corner"](post, plate).blank(post))                  # 2450.0

# Is-a or has-a? A butt joint IS a joint: inherit. A frame HAS beams: hold a list
# (06). Most of the time you want has-a.
