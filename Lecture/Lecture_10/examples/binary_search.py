import timeit

# Linear Search
def linear_search(arr, target):
    """
    Linear search algorithm
    It will check the target value one by one.
    If the target value is found,
    it will return the index of the target value.
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# Binary Search
def binary_search(arr, target):
    """
    Binary search algorithm
    It will check the target valueby dividing the array in half.
    If the target value is found,
    it will return the index of the target value.
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Measure time for linear search
linear_time = timeit.timeit(
    stmt="linear_search(arr, target)",
    setup="from __main__ import linear_search; import random; arr = list(range(1000)); target = random.randint(0, 999)",
    number=1000
)

# Measure time for binary search
binary_time = timeit.timeit(
    stmt="binary_search(arr, target)",
    setup="from __main__ import binary_search; import random; arr = list(range(1000)); target = random.randint(0, 999)",
    number=1000
)

print("Linear Search Time:", linear_time)
print("Binary Search Time:", binary_time)