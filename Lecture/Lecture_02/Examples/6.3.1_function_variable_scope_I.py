x = 0

def foo():
    # the x here is a local variable
    # it is different from the x outside of the function
    x = 100
    print("during the function call, x is ", x)


print("before the function call, x is ", x)
foo()
print("after the function call, x is ", x)
