# Arithmetic operators — the seven you use every day.

a = 9
b = 4

print("Addition:        ", a + b)     # 13
print("Subtraction:     ", a - b)     # 5
print("Multiplication:  ", a * b)     # 36
print("Division (float):", a / b)     # 2.25    -- always a float
print("Division (floor):", a // b)    # 2       -- drops the remainder
print("Modulo:          ", a % b)     # 1       -- the remainder
print("Power:           ", a ** b)    # 6561

# The distinction that catches everyone: /  is true division and always
# returns a float; //  is floor division and drops the remainder.
print(10 / 3)                          # 3.3333333333333335
print(10 // 3)                         # 3


# --- % is the odd/even test, and the "wrap-around" trick -------------------

# In geometry, % is everywhere. Here are the two patterns that recur most.

# 1. Odd or even. Used to offset alternating courses in a brick wall,
#    stripe alternating rows, colour every other panel, etc.
for i in range(6):
    if i % 2 == 0:
        print(f"row {i}: even -- no offset")
    else:
        print(f"row {i}: odd  -- shifted by half a brick")

# 2. Wrap-around. i % n cycles through 0, 1, ..., n-1 and starts again.
#    Useful for laying out items around a circle, choosing from a palette,
#    or picking a colour by index without running off the end.
palette = ["red", "green", "blue"]
for i in range(7):
    colour = palette[i % len(palette)]
    print(f"item {i} -> {colour}")
