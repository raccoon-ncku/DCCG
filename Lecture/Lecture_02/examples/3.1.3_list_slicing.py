# List Slicing
# The full form is  list[start:stop:step]
# - start is INCLUDED, stop is EXCLUDED
# - any of the three parts can be omitted

square = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# --- two-part slices [start:stop] ------------------------------------------

# The start index is inclusive, the end index is exclusive
print("square[2:5] is ", square[2:5])   # [9, 16, 25]

# If you omit the start index, the slice starts from the beginning
print("square[:5] is ", square[:5])     # [1, 4, 9, 16, 25]

# If you omit the end index, the slice goes to the end
print("square[5:] is ", square[5:])     # [36, 49, 64, 81, 100]


# --- three-part slices [start:stop:step] -----------------------------------

# Every second item, from the start
print("square[::2] is ", square[::2])   # [1, 9, 25, 49, 81]

# Every second item, starting at index 1
print("square[1::2] is ", square[1::2]) # [4, 16, 36, 64, 100]

# Every third item within a window
print("square[1:8:3] is ", square[1:8:3])  # [4, 25, 64]


# --- negative indices ------------------------------------------------------

# Negative indices count from the end. -1 is the last, -2 the second-to-last...
print("square[-3:] is ", square[-3:])   # [64, 81, 100]  — last three
print("square[:-2] is ", square[:-2])   # everything except the last two


# --- negative step: reverse ------------------------------------------------

# A step of -1 walks the list backwards. This is the standard "reverse" idiom.
print("square[::-1] is ", square[::-1]) # [100, 81, 64, 49, 36, 25, 16, 9, 4, 1]

# Reversed WINDOW: from index 7 down to (but not including) index 2
print("square[7:2:-1] is ", square[7:2:-1])  # [64, 49, 36, 25, 16]
