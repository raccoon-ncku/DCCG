# print(), type() are built-in functions
# You could use them without defining them.

# You can use the input() function to get input from the user
# and use a variable to store the input
x = input("Please input a number: ")

# The input() function always returns a string
print("The type of x(input) is ", type(x))

# You can use the int() function to convert a string to an integer
x = int(x)
print("The type of x(int) is ", type(x))
