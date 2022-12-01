def func(n):
  i_n2 = 3
  return lambda a, i_n2: a * n * i_n2

doubler = func(2)

print(doubler(11))

tripler = func(3)

print(tripler(11))