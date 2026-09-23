# Fibonacci series:
# the sum of two elements defines the next
a, b = 1, 1
while b < 1000:
    print(b/a)
    a, b = b, a+b # increment a and b

print("end")
