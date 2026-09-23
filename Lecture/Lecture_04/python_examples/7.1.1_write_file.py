"""
Writing a text file — three ways, shortest first.
"""

from pathlib import Path


# --- 1. simplest: Path.write_text ----------------------------------------

# One line, no file handle to remember to close. Good for small strings.
Path("result.txt").write_text("hello, one-liner\n")


# --- 2. `with open(...)` — the everyday form -----------------------------

# `with` closes the file for you, even if an error happens inside the block.
# That is the whole reason it exists. Use it for anything larger than a line.
sample_text = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit,\n"
    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n"
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.\n"
)
with open("result.txt", "w") as fp:
    fp.write(sample_text)


# --- 3. line by line ------------------------------------------------------

# fp.write does NOT add a newline for you -- add "\n" yourself.
lines = ["wall", "slab", "column"]
with open("result.txt", "w") as fp:
    for line in lines:
        fp.write(line + "\n")


# Modes: "r" read (default), "w" write (ERASES first!), "a" append.
# Getting these mixed up is how a term of hand-written notes disappears.
