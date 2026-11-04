"""
The counting pattern — a dictionary whose values grow as you loop.

Turns up constantly: tallying word occurrences, counting vertices per face,
grouping panels by size, histograms of anything.
"""

words = ["wall", "slab", "wall", "column", "slab", "wall"]

# The idiom. `counts.get(word, 0)` returns 0 when a word is unseen,
# so we always have a number to add 1 to.
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)                            # {'wall': 3, 'slab': 2, 'column': 1}


# Same idea, using dict.setdefault -- slightly less idiomatic but useful when
# you want a list to append into rather than a number to increment.
groups = {}
for i, word in enumerate(words):
    groups.setdefault(word, []).append(i)

print(groups)                            # {'wall': [0, 2, 5], 'slab': [1, 4], 'column': [3]}


# For heavy use, collections.Counter and collections.defaultdict do the same
# in one line each -- the stdlib has grown these patterns into first-class
# tools. Reach for them when the loop above becomes noise.
from collections import Counter, defaultdict

print(Counter(words))                    # Counter({'wall': 3, 'slab': 2, 'column': 1})

groups = defaultdict(list)
for i, word in enumerate(words):
    groups[word].append(i)
print(dict(groups))
