import sys

# Get the default recursion limit
print(sys.getrecursionlimit())

# The default value should be 1000
# To change it, use:
print(sys.setrecursionlimit(1000))
