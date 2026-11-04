# Non-default arguments and default arguments
# can be mixed in a function definition.
def foo(a,b,c=0):
    print(a + b + c)

# Yet, non-default arguments 
# must be defined before default arguments.
"""
def bar(a,b=0,c): ; SyntaxError: non-default argument follows default argument
    print(a + b + c)
"""
