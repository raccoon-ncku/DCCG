# enumerate() — when you need the index too.
#
# Reach for it instead of `for i in range(len(items))`.
# It is shorter, and it cannot go out of range.

fonts = ["Times New Roman", "Helvetica", "Fira Code"]
categories = ["Serif", "Sans Serif", "Monospaced"]

for i, font in enumerate(fonts):
    print(f"{i}. {font} is a {categories[i]} font.")

# enumerate can start counting from any number you like:
for n, font in enumerate(fonts, start=1):
    print(f"Font #{n}: {font}")
