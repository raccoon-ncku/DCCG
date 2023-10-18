rows = int(input("input rows: "))

# print upper half of the pattern
for i in range(1, int((rows+1)/2)):
    for j in range(1, i+1):
        print("*", end="--")
    print()

# handle even number of rows
if rows % 2 == 0:
    for j in range(int(rows/2)):
        print("*", end="--")
    print()

# print lower half of the pattern
for i in range(int((rows+1)/2), 0, -1):
    for j in range(1, i+1):
        print("*", end="--")
    print()