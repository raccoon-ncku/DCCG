import math
    
def is_prime(n):
    """
    Check if a number is prime.
    """
    if n == 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def is_prime_optimized(n):
    """
    Check if a number is prime.
    Skip even numbers, and only check up to sqrt(n).
    """
    if n == 1:
        return False
    elif n == 2:
        return True
    elif n > 2 and n % 2 == 0:
        return False
    else:
        max_divisor = math.floor(math.sqrt(n))
        for d in range(3, 1 + max_divisor, 2):
            if n % d == 0:
                return False
        return True