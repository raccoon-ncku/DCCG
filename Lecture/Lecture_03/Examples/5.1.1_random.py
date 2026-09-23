# The `random` module — pseudo-random values, and how to reproduce them.

import random


# --- draw values ---------------------------------------------------------

# random.random() returns a float in [0.0, 1.0)
print(random.random())

# random.randint(a, b) returns an integer in [a, b] (INCLUSIVE on both ends)
random_integer = random.randint(0, 100)
print(random_integer)

# random.choice(seq) picks one element from a sequence
choice = random.choice(["apple", "banana", "cherry"])
print(choice)

# random.shuffle(list) shuffles the list IN PLACE (returns None)
some_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
random.shuffle(some_list)
print(some_list)


# --- seeding: making randomness REPRODUCIBLE -----------------------------

# Without a seed, every run gives different numbers -- you cannot reproduce
# a bug, and you cannot write a deterministic test.
#
# random.seed(N) fixes the starting point. From that call onwards, the
# sequence of "random" values is the same every time you run the program.

random.seed(42)
print(random.randint(1, 6))          # always the same number, every run
print(random.randint(1, 6))          # ... and the next one is also fixed
print(random.choice(["a", "b", "c"]))

# Seed again with the same value and you get the same sequence again.
random.seed(42)
print(random.randint(1, 6))          # matches the first randint above

# This is not a classroom trick -- it is a real engineering habit. Every
# stochastic test in the course seeds first so that a "random" failure
# stays random in the same way, and a fix can be checked.
