# The keyword def introduces a function definition.
# It must be followed by the function name and the parenthesized list of
# formal parameters. The statements that form the body of the
# function start at the next line, and must be __indented__.

def print_hello_world():
    """
    Print hello world.
    This is a docstring. It is a string that is
    the first statement in a function.
    """
    print("Hello World!")

# Now call the function we just defined:
print_hello_world()
