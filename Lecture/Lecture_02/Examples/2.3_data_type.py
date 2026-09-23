# A Python variable has no type; the value it points at does.
# Use type() to ask "what kind of thing is this?"

a = 1
b = 2
c = "3"
d = "4"

# + means addition on numbers and CONCATENATION on strings.
print("a + b =", a + b)          # 3   -- number + number
print("c + d =", c + d)          # 34  -- string + string, NOT 7

# Mixing types with + is an error: Python will not guess for you.
# print(a + c)  # TypeError: unsupported operand type(s) for +: 'int' and 'str'

# Convert first, then combine
print("a + int(c) =", a + int(c))    # 4
print("str(a) + c =", str(a) + c)    # '13'  -- both strings now


# --- inspect a value ------------------------------------------------------

# type() reports the class of a value.
print("type(a) is", type(a))     # <class 'int'>
print("type(c) is", type(c))     # <class 'str'>

# The f"{name=}" debug form prints the expression AND its value in one shot.
# This is the single fastest debugging tool in the language.
print(f"{a=}")                   # a=1
print(f"{c=} {type(c)=}")        # c='3' type(c)=<class 'str'>


# --- floats are approximate. Remember this. -------------------------------

# Decimals do not divide evenly into binary. Every language has this.
print(0.1 + 0.2)                 # 0.30000000000000004
print(0.1 + 0.2 == 0.3)          # False !

# NEVER compare computed floats with ==. Use a tolerance:
print(abs((0.1 + 0.2) - 0.3) < 1e-9)   # True
