# Logical operators — combining conditions.
# The three you need: and, or, not.

x = int(input("Please enter an integer: "))

# --- and: BOTH conditions must be true ------------------------------------

if x > 0 and x % 3 == 0:
    print("x is a positive number AND a multiple of 3")


# --- or: at least one condition must be true ------------------------------

if x < -20 or x > 20:
    print("x is larger than 20 or smaller than -20")


# --- not: inverts a boolean ------------------------------------------------

# These two branches are equivalent.
if x > 0 and x % 3 != 0:
    print("x is a positive number and NOT a multiple of 3   (via !=)")
if x > 0 and not x % 3 == 0:
    print("x is a positive number and NOT a multiple of 3   (via not)")


# --- chained comparisons: Python allows a < x < b -------------------------

# Most languages force you to write   0 < x and x < 10.
# Python lets you chain them, and it reads more like maths.
if 0 < x < 10:
    print("x is between 0 and 10 (exclusive)")

if -10 <= x <= 10:
    print("x is between -10 and 10 (inclusive)")


# --- short-circuit evaluation ---------------------------------------------

# In `A and B`, if A is False Python does NOT evaluate B.
# In `A or B`,  if A is True  Python does NOT evaluate B.
# You use this to guard against errors: check that a list is non-empty
# BEFORE trying to index into it.
items = []
if items and items[0] > 0:               # items[0] is never reached
    print("first item is positive")
