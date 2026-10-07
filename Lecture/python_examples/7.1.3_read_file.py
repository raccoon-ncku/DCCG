"""
Reading a text file — three ways, shortest first.
"""

from pathlib import Path


# --- 1. simplest: read the whole thing as a string -----------------------

text = Path("result.txt").read_text()
print(text)


# --- 2. `with open(...)` for the whole file -----------------------------

with open("result.txt") as fp:      # "r" mode is the default
    content = fp.read()
print(content)


# --- 3. line by line (memory-friendly on big files) ---------------------

# The idiomatic loop: iterating a file yields ONE LINE at a time. Each line
# ends in "\n" -- .rstrip() drops it (and any trailing whitespace).
with open("result.txt") as fp:
    for line in fp:
        print(line.rstrip())


# --- .readlines() when you want the whole file as a list of strings -----

# Loads everything into memory -- fine for small files, wasteful for huge ones.
lines = Path("result.txt").read_text().splitlines()   # no trailing "\n"
for i, line in enumerate(lines):
    print(f"{i}: {line}")
