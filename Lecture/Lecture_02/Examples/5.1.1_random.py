import random

# random.randint takes two arguments, a lower and upper bound
# random.randint returns a random integer between the two bounds
random_integer = random.randint(0, 100)
print(random_integer)

# random.choice takes a list as an argument
# random.choice returns a random element from the list
choice = random.choice(["apple", "banana", "cherry"])
print(choice)

# random.shuffle takes a list as an argument
# random.shuffle shuffles the list in place
some_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
random.shuffle(some_list)
print(some_list)