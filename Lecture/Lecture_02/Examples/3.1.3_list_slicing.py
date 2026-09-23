# List Slicing
square = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# In python, we use [start:end] to slice a list
# The start index is inclusive, the end index is exclusive
print("square[2:5] is ", square[2:5])

# If you omit the start index, the slice starts from the beginning
print("square[:5] is ", square[:5])

# If you omit the end index, the slice goes to the end
print("square[5:] is ", square[5:])
