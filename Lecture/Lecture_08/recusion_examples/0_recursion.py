"""
Recursion — a function that calls itself on a smaller version of the same problem.

Every recursive function needs exactly two things:
  1. A BASE CASE small enough to answer outright.
  2. A RECURSIVE CASE that moves TOWARD the base case.

Miss either one and you get RecursionError.
"""


def factorial(n):
    """Return n! = n * (n-1) * ... * 1.

    factorial(0) == 1     (mathematical convention: the empty product)
    factorial(1) == 1
    factorial(5) == 120
    """
    if n < 0:
        raise ValueError(f"factorial is not defined for negative n; got {n}")
    if n <= 1:                        # BASE CASE — covers both 0 and 1
        return 1
    print(f"{n}! = {n} * {n - 1}!")   # trace: on the way DOWN
    return n * factorial(n - 1)       # RECURSIVE CASE — smaller problem


print("factorial(4) =", factorial(4))    # 24
print()
print("factorial(0) =", factorial(0))    # 1  -- was buggy in the old file
print("factorial(1) =", factorial(1))    # 1


# --- countdown vs countup: where you put the work matters ---------------

# Same structure, one line moved, opposite output.
# The rule: anything AFTER the recursive call runs during the UNWINDING —
# on the way back UP.

def countdown(n):
    if n == 0:
        return
    print(n, end=" ")                 # printed BEFORE the recursion
    countdown(n - 1)                  # -> 3 2 1

def countup(n):
    if n == 0:
        return
    countup(n - 1)                    # recurse FIRST
    print(n, end=" ")                 # printed on the way back up -> 1 2 3


print()
print("countdown:", end=" "); countdown(3); print()
print("countup:  ", end=" "); countup(3); print()
