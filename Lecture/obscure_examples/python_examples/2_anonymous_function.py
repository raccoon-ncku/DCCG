def func(n):
    return lambda a : a * n

doubler = func(2)

print(doubler(11))

tripler = func(3)

print(tripler(11))