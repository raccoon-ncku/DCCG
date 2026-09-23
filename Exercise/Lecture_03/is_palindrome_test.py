from is_palindrome import is_palindrome

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

test_cases = [
    ("", True),
    ("a", True),
    ("aa", True),
    ("ab", False),
    ("aba", True),
    ("abc", False),
    ("abba", True),
    ("abcba", True),
    ("abbcba", False),
    ("never odd or even", True),
    ("never even or odd", False),
    ("rats live on no evil star", True),
    ("rats live on no evil tsar", False),
    ("Racecar", True),
    ("A man a plan a canal Panama", True)
]

def test_is_palindrome():
    for test_string, expected_result in test_cases:
        print("Testing \"{}\"\t".format(test_string), end="")
        result = is_palindrome(test_string)
        if result == expected_result:
            print("{}PASS{}".format(Colors.GREEN, Colors.RESET))
        else:
            print("{}FAIL{} (expected \033[94m{}\033[0m, got \033[93m{}\033[0m)".format(Colors.RED, Colors.RESET, expected_result, result))
            return

test_is_palindrome()