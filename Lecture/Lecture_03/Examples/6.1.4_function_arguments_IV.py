def foo(a,b,c=0):
    print(a + b + c)

# when calling a function, 
# we can specify arguments by position or by keyword
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