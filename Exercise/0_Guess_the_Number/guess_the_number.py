import random

answer = random.randint(0, 100)

game_over = False

lower_bound = 0
upper_bound = 100

while not game_over:
    x = int(input("Please enter an integer({} - {}): ".format(lower_bound, upper_bound)))
    if x <= lower_bound or x >= upper_bound:
        continue
    elif x > answer:
        upper_bound = x
    elif x < answer:
        lower_bound = x
    elif x == answer:
        game_over = True

print("The answer is {}".format(answer))
