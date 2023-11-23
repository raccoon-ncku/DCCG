def factorial(x):
    """
    This is a recursive function
    to find the factorial of an integer
    """

    if x == 1:
        # Base case
        return 1
    else:
        # Recursive case
        print(f"{x}! = {x} * {(x-1)}!")
        return x * factorial(x-1)


num = 12
print(f"The factorial of {num} is {factorial(num)}")
