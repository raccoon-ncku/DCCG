def solve_tower_of_hanoi(n , source, destination, auxiliary):
    """
    Solves the Tower of Hanoi puzzle recursively.
    
    Parameters:
    - n (int): Number of disks to be moved.
    - source (str): Name of the source peg.
    - destination (str): Name of the destination peg.
    - auxiliary (str): Name of the auxiliary peg.
    """
    
    # Base case: Only one disk to be moved
    if n==1:
        print ("Move disk 1 from source",source,"to destination",destination)
        return
    
    # Move n-1 disks from source to auxiliary using destination as auxiliary
    solve_tower_of_hanoi(n-1, source, auxiliary, destination)
    print("Move disk",n,"from source",source,"to destination",destination)

    # Move n-1 disks from auxiliary to destination using source as auxiliary
    solve_tower_of_hanoi(n-1, auxiliary, destination, source)
         
# Driver code
N = 3
# A, C, B are the name of rods
solve_tower_of_hanoi(N,'A','C','B') 
