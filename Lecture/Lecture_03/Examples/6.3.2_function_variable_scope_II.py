x = 0

def function():
    # Local variables are not accesible outside of the function
    y=0
    # x could be accessed, but not modified
    print("During the function call, x is", x)

function()
print(y) # This will cause error
