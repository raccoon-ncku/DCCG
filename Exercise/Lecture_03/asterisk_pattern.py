rows = int(input("Enter the number of rows: "))

if rows % 2 == 0:
    for i in range(1, int(rows/2)+1):
        for j in range(1, i + 1):
            print("*", end = " ")
        print()
    for i in range(int(rows/2), 0, -1):
        for j in range(1, i + 1):
            print("*", end = " ")
        print()
elif rows % 2 == 1:
    for i in range(1, int((rows + 1)/2)):
        for j in range(1, i + 1):
            print("*", end = " ")
        print()
    for i in range(int((rows + 1)/2), 0, -1):
        for j in range(1, i + 1):
            print("*", end = " ")
        print()
else:
    print("Invalid input")