import random

answer = random.randint(0, 100)

game_over = False

lower_limit = 0
upper_limit = 100

while not game_over:
    user_answer = int(input("please input an integer({} - {}):".format(lower_limit, upper_limit)))
    if user_answer > upper_limit or user_answer < lower_limit:
        print(":(")
        continue
    elif answer == user_answer:
        game_over = True
    elif user_answer > answer:
        upper_limit = user_answer
        print("too high")
    elif user_answer < answer:
        lower_limit = user_answer
        print("too small")

print("You win!")