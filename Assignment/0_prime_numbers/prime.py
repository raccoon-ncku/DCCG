import math


def is_prime(n):
    """
    Determine if the given n is a prime number

    ### Parameters
    1. n : int
        - the number to be checked

    ### Returns
    - bool
        - True if the given n is a prime number
    """
    if n <= 1:
        return False
    elif n == 2:
        return True
    else:
        is_prime = True
        for i in range(2, int(math.ceil(math.sqrt(n)))+1):
            if n % i == 0:
                is_prime = False
                break
        return is_prime


if __name__ == "__main__":
    upper_bound = input("please input an integer:")
    prime = [2]
    for i in range(3, int(upper_bound)):
        if is_prime(i):
            prime.append(i)
    print("There are {} prime numbers smaller than {}, they are:\n{}".format(
        len(prime), upper_bound, prime))
