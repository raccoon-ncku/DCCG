# A string is a sequence of characters.


name = "wall" # You can use single or double quotes to represent strings.
count = 12


# Formatting a string
# The "".format() method is used to format a string.
# The {} is a placeholder for the variable.
# The order of the variables is the same as the order of the variables in the format() method.

# f-strings: put an f before the quote, then {expressions} inside
print(f"The {name} has {count} bricks.")
print(f"Half of that is {count / 2}.")
print(f"Rounded to 2 decimals: {3.14159:.2f}")   # 3.14

# use formating to compose a more complex string
# it is more **readable** than using + to concatenate strings
# use cases: logging, debugging, etc.
