even_number_flag = False

numbers = [1,3,5,7,9,10,11,13]

for number in numbers:
    if number % 2 == 0:
        even_number_flag = True

if even_number_flag:
    print("There is at least one even number in the list.")
else:
    print("They are all odd numbers.")