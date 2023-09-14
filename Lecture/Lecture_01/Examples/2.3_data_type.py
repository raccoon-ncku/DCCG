# Python varialbe has no type, but the data(value) has type.

a = 1
b = 2
c = "3"
d = "4"

print("a + b = ", a + b)
print("c + d = ", c + d)

# The following line will cause an error
print("a + c = ", a + c)

# You can use the type() function to check the type of a variable
print("The type of a is ", type(a))
print("The type of c is ", type(c))