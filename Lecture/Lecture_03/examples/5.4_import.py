# use as to give a module a different name
import datetime as dt

# use the alias to access the datetime class
now = dt.datetime.now()

# you can also partially import a module
from random import randint

# randint is now available without the dot notation
# other functions from random are not available
random_integer = randint(0, 100)
