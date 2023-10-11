# A function can have optional arguments,
# which can have default values.
def fib(n=10000):
    """
    Print a Fibonacci series up to n.
    """
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

# Call the function while omitting the optional argument:
fib()

# Call the function while specifying the optional argument:
fib(100)
