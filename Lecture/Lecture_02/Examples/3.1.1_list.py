# Python knows a number of compound data types,
# used to group together other values.
# The most versatile is the list, which can be
# written as a list of comma-separated values (items)
# between square brackets.
# Lists might contain items of different types,
# but usually the items all have the same type.

squares = [1, 4, 9, 16, 25]

# Accessing elements in a list
# Python uses zero-based indexing
print("squares[0] is ", squares[0])

# Negative indices count from the end of the list
print("squares[-1] is ", squares[-1])
print("squares[-3] is ", squares[-3])

# Use function "len()" Get the item count of a list
print("len(squares) is ", len(squares))
