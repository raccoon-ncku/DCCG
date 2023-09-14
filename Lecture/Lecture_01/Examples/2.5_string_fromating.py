# A string is a sequence of characters.

# You can use single or double quotes to represent strings.
a = "foo"
b = 'bar'

# Formatting a string
# The "".format() method is used to format a string.
# The {} is a placeholder for the variable.
# The order of the variables is the same as the order of the variables in the format() method.
print("a = {}, b = {}".format(a, b))

# without the format() method, you have to use + to concatenate strings
print("a = " + a + ", b = " + b)

# use formating to compose a more complex string
# it is more **readable** than using + to concatenate strings
# use cases: logging, debugging, etc.
