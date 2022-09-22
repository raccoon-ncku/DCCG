def increment(x):
    x = x+1
    print("during the function call, x is ", x)
    return x

x = 0
print("brfore the function call, x is ", x)
x = increment(x)
print("after the function call, x is ", x)
