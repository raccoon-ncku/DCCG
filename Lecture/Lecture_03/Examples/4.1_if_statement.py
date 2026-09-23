# if / elif / else — the decision structure.

# --- 1. bare if -----------------------------------------------------------

x = 10
if x > 0:
    print("x is a positive number")

y = -5
if y > 0:
    print("y is a positive number")     # this line does NOT print
# (nothing happens when the condition is false; execution just continues)


# --- 2. if / else ---------------------------------------------------------

# else covers "everything the if did not cover".
n = -3
if n >= 0:
    print(f"{n} is not negative")
else:
    print(f"{n} is negative")


# --- 3. if / elif / else — a cascade -------------------------------------

# elif branches are tested in ORDER. Only the FIRST true branch runs;
# everything below it is skipped.
temperature = 18

if temperature > 25:
    print("hot")
elif temperature > 15:
    print("mild")               # <- 18 > 15 is true, so this prints
elif temperature > 5:
    print("cool")               # skipped, even though it is also true
else:
    print("cold")


# --- 4. ORDER changes behaviour ------------------------------------------

# The exact same conditions, reordered, produce different output.
# Swap the two branches and every mild day now prints "hot".
temperature = 18

if temperature > 15:
    print("15+ -> would print 'mild' first")
elif temperature > 25:
    print("25+ -> never reached, because 15+ already caught it")


# --- 5. common gotchas ---------------------------------------------------

# The colon at the end of the line is required.
# The body must be INDENTED (4 spaces). Python has no braces.
# = assigns, == compares. `if x = 5:` is a syntax error.
