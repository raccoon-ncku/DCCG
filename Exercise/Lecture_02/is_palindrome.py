def is_palindrome(string):
    """
    Return True if string is a palindrome, False otherwise.
    """
    # Remove spaces
    string = string.replace(" ", "")
    # convert to lower case
    string = string.lower()
    # Check if string is a palindrome
    for i in range(len(string) // 2):
        if string[i] != string[-i - 1]:
            return False
    return True