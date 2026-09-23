import random

# Generate a random number between 1 and 100
random_number = random.randint(1, 100)
current_range = [0, 100]

while True:
    # Ask user to guess a number
    guess = int(input(
        "Guess a number between {} and {}: ".format(
            current_range[0], current_range[1])))

    # Check if the guess is correct
    if guess == random_number:
        print("You guessed correctly!")
        break
    elif guess > random_number:
        current_range[1] = guess
        print("Your guess is too high!")
    else:
        current_range[0] = guess
        print("Your guess is too low!")
