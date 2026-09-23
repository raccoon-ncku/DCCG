# while — repeat as long as a condition is true.
#
# Use it when you do NOT know in advance how many repetitions you need.
# Every while loop needs something that eventually makes the condition false.
# If you write an infinite loop by accident, ctrl+C stops it.


# --- the classic pattern: "keep adding until we have enough" --------------

total = 0
n = 1
while total < 100:
    total += n
    n += 1
print(f"needed {n - 1} terms; total is {total}")


# --- Fibonacci: also a natural fit for while -----------------------------

# We do not know in advance how many terms it takes to exceed 1000, so
# we loop until the value itself makes the condition false.
a, b = 1, 1
while b < 1000:
    print(b, end=" ")
    a, b = b, a + b        # unpacking assignment: compute both, then assign
print()
print("end")


# --- guard against an infinite loop --------------------------------------

# ALWAYS ask: what makes this condition eventually false?
# Here the counter goes up; if you accidentally decrement it, you loop forever.
count = 5
while count > 0:
    print(count)
    count -= 1            # <-- the step that ends the loop
