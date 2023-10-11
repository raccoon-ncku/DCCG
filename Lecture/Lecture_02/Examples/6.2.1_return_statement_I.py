# A function could return a value,
# which can be assigned to a variable.

def fib(n=10000):
    """
    Return a Fibonacci series up to n.
    """
    a, b = 0, 1
    series = []
    while a < n:
        series.append(a)
        a, b = b, a+b
    return series

fib_series = fib(10000)
print(fib_series)
