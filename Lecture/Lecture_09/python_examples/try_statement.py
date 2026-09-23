nums = [3,2,1,0]

for num in nums:
    print(3/num)

for num in nums:
    try:
        print(3/num)
    except:
        print("You can't divide by zero!")