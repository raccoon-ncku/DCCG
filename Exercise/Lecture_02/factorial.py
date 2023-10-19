def factorial(n=0):
    """
    Return the factorial of the given number.
    """

    if n < 0:
        print("Factorial is not defined for negative numbers.")
        return None

    result = 1
    for i in range(1, n+1):
        # the next line is equivalent to result = result * i
        result *= i

    return result


# Test the function
print(factorial(-5))
print(factorial())  # using the default value 0
print(factorial(1))
print(factorial(5))
