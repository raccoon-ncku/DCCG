while True:
    try:
        e = float(input("Please input a number: "))       
    except ValueError:
        print("Can't convert it into a valid integer, please try again")
        continue
    else:
        break
e = int(e)
print("The value of e is {} and its type is {}".format(e, type(e)))