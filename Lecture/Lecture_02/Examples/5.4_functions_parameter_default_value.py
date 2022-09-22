def fib(n=10000):
    """
    Print a Fibonacci series up to n.
    """
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

# Now call the function we just defined:
fib()
