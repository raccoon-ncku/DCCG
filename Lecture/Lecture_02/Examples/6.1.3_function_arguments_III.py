# Optioanl arguments should be 
# at the end of the argument list
def foo(a,b,c=0):
    print(a + b + c)

# Invalid Function Definitions
'''
def bar(a,b=0,c):
    print(a + b + c)
'''

# While calling a function, there are two ways to pass arguments:
# 1. Positional arguments
# 2. Keyword arguments
# Positional arguments should be 
# at the beginning of the argument list

foo(1,2) # omitting the optional argument c
foo(1,2,3)
foo(a=1,b=2) # omitting the optional argument c
foo(a=1,b=2,c=3)
foo(c=1,b=2,a=3) # order of keyword arguments does not matter
foo(1,b=2,c=3) # mixing positional and keyword arguments
foo(1,2,c=3) # mixing positional and keyword arguments

# Invalid Calls
foo(a=1,2) # SyntaxError: positional argument follows keyword 
foo(a=1,2,c=3) # SyntaxError: positional argument follows keyword argument
foo(1, c=3) # missing 1 required positional argument: 'b'