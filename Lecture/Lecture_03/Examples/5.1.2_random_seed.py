import random

# random.seed sets the seed of the random number generator
# setting the seed to a constant value will result in the same random numbers
# being generated every time the program is run.
# Its useful for debugging.
random.seed(1)
print(random.random())