"""
A tuple is a collection which is ordered and unchangeable.

Tuples are written with round brackets.
"""

tuple = (0, 1, 2, 3)

for i in range(len(tuple)):
    # Tuple items are indexed
    print(tuple[i])

# Tuples are unchangeable,
# meaning that we cannot change, add or remove items after the tuple has been created.
tuple[0] = 10  # won't run
