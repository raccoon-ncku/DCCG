squares = [1, 4, 9, 16, 25]

# The append() method appends an element to the end of the list.
squares.append(36)
print("After .append(36), squares is", squares)

# The pop() method removes the specified index.
# If you do not specify the index, the pop() method removes the last item.
squares.pop()
print("After .pop(), squares is", squares)

squares.pop(0)
print("After .pop(0), squares is", squares)

# The index()) method finds the first occurrence of the specified value.
# The index() method raises an exception if the value is not found.
print("squares.index(16) is", squares.index(16))
print("squares.index(100) is", squares.index(100))