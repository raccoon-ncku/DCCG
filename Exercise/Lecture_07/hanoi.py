# Recursive Python function to solve the tower of hanoi
 
states = []
counters = [0]

def TowerOfHanoi(n , source, destination, auxiliary):
    if n==1:
        print ("Move disk 1 from source",source,"to destination",destination)
        new_state = states[-1].copy()
        new_state[source].pop()
        new_state[destination].append(n)
        states.append(new_state)
        print(states[-1])
        counters.append(counters[-1] + 1)
        return
    TowerOfHanoi(n-1, source, auxiliary, destination)
    print("Move disk",n,"from source",source,"to destination",destination)
    
    new_state = states[-1].copy()
    new_state[source].pop()
    new_state[destination].append(n)
    states.append(new_state)
    counters.append(counters[-1] + 1)
    print(states[-1])
    TowerOfHanoi(n-1, auxiliary, destination, source)
         
# Driver code
n = 4
states.append(
    {
        "A": [4, 3, 2, 1],
        "B": [],
        "C": []
    }
)
TowerOfHanoi(n,'A','B','C') 
# A, C, B are the name of rods
print(states)
# Contributed By Dilip Jain