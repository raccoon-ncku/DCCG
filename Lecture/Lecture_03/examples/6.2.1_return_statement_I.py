# A function could return a value,
# which can be assigned to a variable.

def is_even(number):
    """
    Return True if the number is even, False otherwise.
    """
    if number % 2 == 0:
        return True
    else:
        return False
    
# Call the function and assign the return value to a variable.
number = int(input("Enter a number: "))
result = is_even(number)
if result:
    print("{} is even.".format(number))
else:
    print("{} is odd.".format(number))
