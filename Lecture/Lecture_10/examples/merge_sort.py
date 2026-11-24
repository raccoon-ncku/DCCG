"""Divide and conquer: merge sort.

Split the list in half, sort each half the same way, merge the two sorted
halves. Insertion sort is here to compare: both count their comparisons.
W10 README §3.
"""


def merge(left, right, counter):
    """One sorted list from two sorted lists, taking the smaller front item each time."""
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        counter[0] += 1
        if right[j] < left[i]:
            out.append(right[j])
            j += 1
        else:
            out.append(left[i])         # on a tie, left first: equal items keep their order
            i += 1
    return out + left[i:] + right[j:]


def merge_sort(items, counter=None, trace=None, depth=0):
    """A sorted copy of items.

    counter, if given, is a one-item list that adds up the comparisons; trace,
    a list that receives (depth, merged) after every merge.
    """
    counter = [0] if counter is None else counter
    items = list(items)
    if len(items) <= 1:
        return items                    # one item is already sorted: the recursion stops
    mid = len(items) // 2
    left = merge_sort(items[:mid], counter, trace, depth + 1)
    right = merge_sort(items[mid:], counter, trace, depth + 1)
    merged = merge(left, right, counter)
    if trace is not None:
        trace.append((depth, merged))
    return merged


def insertion_sort(items, counter=None):
    """A sorted copy of items, made by inserting each item into the sorted part before it."""
    counter = [0] if counter is None else counter
    out = list(items)
    for i in range(1, len(out)):
        j = i
        while j > 0:
            counter[0] += 1
            if out[j] < out[j - 1]:
                out[j], out[j - 1] = out[j - 1], out[j]
                j -= 1
            else:
                break
    return out
