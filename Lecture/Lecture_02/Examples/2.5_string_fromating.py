# Strings — formatting, and the handful of methods you use every week.


name = "wall"           # single or double quotes both make a string
count = 12


# --- f-strings -------------------------------------------------------------

# Put an f before the quote, then write {expressions} inside the string.
# Anything Python can evaluate can go inside the braces.

print(f"The {name} has {count} bricks.")
print(f"Half of that is {count / 2}.")

# Format specifiers after a colon control how the value is shown.
# ".2f"  = float, 2 decimal places
# "05d"  = integer, zero-padded to width 5
print(f"Rounded to 2 decimals: {3.14159:.2f}")   # 3.14
print(f"Zero-padded id: {count:05d}")            # 00012


# --- the {var=} debug form -------------------------------------------------

# The = inside the braces prints the expression AND its value.
# The fastest way to check what a variable really holds.
width = 10
print(f"{width=}")                       # width=10
print(f"{width=} {type(width)=}")        # width=10 type(width)=<class 'int'>


# --- string methods ---------------------------------------------------------

# Change case
print("hello".upper())                   # 'HELLO'
print("HELLO".lower())                   # 'hello'

# Trim whitespace at both ends -- reading files gives you a trailing "\n"
print("  padded  ".strip())              # 'padded'

# Split a string into a list, and join a list back into a string.
# These two are the pair you reach for when parsing CSV, paths, filenames.
print("a,b,c".split(","))                # ['a', 'b', 'c']
print("-".join(["a", "b", "c"]))         # 'a-b-c'

# len() returns the number of characters in a string
print(len("hello"))                      # 5

# Replace, and check contents
print("wall".replace("w", "W"))          # 'Wall'
print("wall" in "wallpaper")             # True
