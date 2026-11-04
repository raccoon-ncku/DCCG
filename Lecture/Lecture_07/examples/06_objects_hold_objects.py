"""Objects hold other objects, by reference. Follow those references and you have a graph.

    uv run Lecture/Lecture_07/examples/06_objects_hold_objects.py
"""

import copy
import math


class Beam:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Beam({self.name!r})"

    @property
    def length(self):
        return math.dist(self.start, self.end)


# --- a name is a label on an object, not a copy of it --------------------------
post = Beam("post", (0, 0, 0), (0, 0, 2400))
same = post
twin = copy.copy(post)
post.end = (0, 0, 3000)
print(same.length)                      # 3000.0: same object, two names
print(twin.length)                      # 2400.0: a separate object


# --- has-a: a joint HAS two beams ----------------------------------------------
class Joint:
    def __init__(self, a, b):
        self.a = a                      # not a copy: the beam itself
        self.b = b

    def __repr__(self):
        return f"Joint({self.a.name}, {self.b.name})"

    def other(self, beam):
        return self.b if beam is self.a else self.a


# --- a frame has beams and joints, which is a graph in all but name ------------
class Frame:
    def __init__(self):
        self.beams = []
        self.joints = []

    def add(self, name, start, end):
        beam = Beam(name, start, end)
        self.beams.append(beam)
        return beam

    def join(self, a, b):
        self.joints.append(Joint(a, b))

    def neighbours(self, beam):
        return [joint.other(beam) for joint in self.joints if beam in (joint.a, joint.b)]


frame = Frame()
sill = frame.add("sill", (0, 0, 0), (3600, 0, 0))
post = frame.add("post", (0, 0, 0), (0, 0, 2400))
cap = frame.add("cap", (0, 0, 2400), (3600, 0, 2400))
frame.join(post, sill)
frame.join(post, cap)

print(frame.joints)                     # [Joint(post, sill), Joint(post, cap)]
print(frame.neighbours(post))           # [Beam('sill'), Beam('cap')]

# Move the beam and the joint sees it, because it holds the beam and not a copy.
post.end = (0, 0, 2700)
print(frame.joints[1].a.length)         # 2700.0


# --- the trap: a mutable default is shared by every object (Week 03) -----------
class BadFrame:
    def __init__(self, beams=[]):       # one list, made once, when Python reads this line
        self.beams = beams


first, second = BadFrame(), BadFrame()
first.beams.append("post")
print(second.beams)                     # ['post']: second never added anything
