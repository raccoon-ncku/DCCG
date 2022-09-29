def increment(input_x):
    output_x = input_x+1
    print("during the function call, x is ", output_x)
    return output_x

x = 0
print("brfore the function call, x is ", x)
x = increment(input_x = x)
print("after the function call, x is ", x)
