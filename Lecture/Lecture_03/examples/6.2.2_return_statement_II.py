# return statement could also 
# be used to exit a function early.

def find_first_negative_number(numbers):
    """
    Return the first negative number in the list of numbers.
    """
    for number in numbers:
        if number < 0:
            return number # return statement exits the function
    return "No negative number found."

numbers = [1, 2, 3, -4, 5, 6, 7, 8, 9]
print(find_first_negative_number(numbers))
