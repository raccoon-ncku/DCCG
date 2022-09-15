# The keyword def introduces a function definition.
# It must be followed by the function name and the parenthesized list of
# formal parameters. The statements that form the body of the
# function start at the next line, and must be __indented__.

def fib(n):
    """
    Print a Fibonacci series up to n.
    return nothing
    """
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

# Now call the function we just defined:


fib(10000)
# result = fib(10000)
# print("The result is :", result)


def fib2(n):  # return Fibonacci series up to n
    """Return a list containing the Fibonacci series up to n."""
    result = []
    a, b = 0, 1
    while a < n:
        a, b = b, a+b
    result = b / a
    return result


golden_ratio = fib2(10000)
print(golden_ratio)
