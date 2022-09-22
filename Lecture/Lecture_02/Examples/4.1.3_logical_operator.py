x = int(input("Please enter an integer: "))

if x > 0 and x % 3 == 0:
    print("x is a postive number and a multiple of 3")

if x > 0 and not x % 3 == 0:
    print("x is a postive number and not a multiple of 3")

if x < -20 or x > 20:
    print("x is larger than 20 or smaller than -20")