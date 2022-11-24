def func(n):
  i_n2 = 3
  return lambda a, n2=i_n2: a * n * n2

doubler = func(2)

print(doubler(11))

tripler = func(3)

print(tripler(11))