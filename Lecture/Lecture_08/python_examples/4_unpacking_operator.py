def num_sum(num1,num2,num3,num4,num5):
    return num1 + num2 + num3 + num4 + num5

num_list = [1,2,3,4,5]

print(num_sum(num_list[0], num_list[1], num_list[2], num_list[3], num_list[4])
)

print(num_sum(*num_list))