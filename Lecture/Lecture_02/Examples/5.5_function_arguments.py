def foo(a,b,c=0):
    print(a + b + c)

foo(1,2)
foo(1,2,3)
foo(a=1,b=2)
foo(a=1,b=2,c=3)
foo(1,b=2,c=3)
foo(1,2,c=3)

# Invalid Calls
foo(a=1,2) # SyntaxError: positional argument follows keyword 
foo(a=1,2,c=3) # SyntaxError: positional argument follows keyword argument
foo(1, c=3) # missing 1 required positional argument: 'b'