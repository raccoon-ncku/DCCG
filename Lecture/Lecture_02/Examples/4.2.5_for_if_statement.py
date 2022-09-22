for i in range(40):
    for j in range(40):
        if i % 5 == 0 and j % 5 == 0:
            print('*', end='')
        elif i % 5 == 0:
            print('-', end='')
        elif j % 5 == 0:
            print('|', end='')
        else:
            print('.', end='')
    print()