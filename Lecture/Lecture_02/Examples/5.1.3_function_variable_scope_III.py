x = 0

def function():
    # Local variables are not globally accesible
    y=0
    print(x)

function()
print(x)
print(y) # This will cause errort("after the function call, x is ", x)
