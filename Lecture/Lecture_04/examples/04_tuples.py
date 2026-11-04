"""
Tuples — like lists, but unchangeable. Round brackets.

Use a tuple when the collection is a fixed record (a coordinate, an RGB
colour) rather than a growing sequence. Tuples can be dictionary keys;
lists cannot.
"""

# A tuple, used as a coordinate.
point = (3.0, 4.0, 0.0)


# --- unpacking (the usual way to read a tuple) ----------------------------

x, y, z = point                    # names the three components in one line
print(x, y, z)

# Same idea in a loop: unpack while iterating.
points = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0)]
for px, py, pz in points:
    print(f"({px}, {py}, {pz})")


# --- immutable, on purpose ------------------------------------------------

try:
    point[0] = 10                  # TypeError -- tuples are unchangeable
except TypeError as e:
    print("Cannot change a tuple:", e)


# --- tuples can be dictionary keys; lists cannot -------------------------

# Because a tuple's contents cannot change, its hash is stable, and Python
# lets it index into a dict. Handy for grid coordinates or panel IDs.
grid = {}
grid[(0, 0)] = "corner"
grid[(0, 1)] = "edge"
grid[(1, 1)] = "interior"
print(grid[(0, 0)])                # 'corner'


# --- multiple return values are tuples -----------------------------------

def bounds(numbers):
    return min(numbers), max(numbers)      # a tuple

lo, hi = bounds([3, 1, 4, 1, 5, 9, 2, 6])
print(f"lo={lo}, hi={hi}")
