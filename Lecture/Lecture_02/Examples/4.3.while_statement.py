# Fibonacci series:
# the sum of two elements defines the next
a, b = 1, 1
while a < 1000000:
    print(b/a)
    a, b = b, a+b

print("end")
