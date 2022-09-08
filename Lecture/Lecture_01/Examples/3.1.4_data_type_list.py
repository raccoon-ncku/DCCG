# Python knows a number of compound data types,
# used to group together other values.
# The most versatile is the list, which can be
# written as a list of comma-separated values (items)
# between square brackets.
# Lists might contain items of different types,
# but usually the items all have the same type.

squares = [1, 4, 9, 16, 25]

# Accessing elements in a list 
print("squares[0] is ", squares[0])
print("squares[-1] is ", squares[-1])

# Use function "len()" Get the length of a list
print("len(squares) is ", len(squares))

# The append() method appends an element to the end of the list.
squares.append(36)
print("After .append(36), squares is", squares)

# The pop() method removes the specified index.
# If you do not specify the index, the pop() method removes the last item.
squares.pop()
print("After .pop(), squares is", squares)

squares.pop(0)
print("After .pop(0), squares is", squares)