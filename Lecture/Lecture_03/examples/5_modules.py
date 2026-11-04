# Modules — how you use other people's code.
#
# A module is a file of Python you can use from another file.
# The standard library ships with hundreds.


# --- three ways to import ------------------------------------------------

# 1. import the whole module. Refer to its contents via the module name.
import math
print(math.pi)                 # 3.141592653589793
print(math.sqrt(16))           # 4.0
print(math.cos(0))             # 1.0

# 2. import specific names into the current file
from math import pi, cos, radians
print(pi)                      # 3.141592653589793
print(cos(radians(90)))        # ~0 (near-zero, floats are approximate)

# 3. import the module under a shorter alias
import math as m
print(m.floor(3.9))            # 3
print(m.ceil(3.1))             # 4


# --- another useful stdlib module ----------------------------------------

# random.random() returns a float in [0.0, 1.0)
import random
print(random.random())


# --- angles are in RADIANS ----------------------------------------------

# math.sin, math.cos, and COMPAS all take radians, not degrees.
# math.radians(90) converts.
# Forgetting this produces geometry that is wrong but not obviously wrong.
print(math.sin(math.radians(90)))    # 1.0
print(math.sin(90))                  # 0.8939...  -- 90 RADIANS, meaningless
