import copy

states = []

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
        new_state = copy.deepcopy(states[-1])
        new_state[source].pop()
        new_state[destination].append(n)
        states.append(new_state)
        return
    
    # Move n-1 disks from source to auxiliary using destination as auxiliary
    solve_tower_of_hanoi(n-1, source, auxiliary, destination)
    print("Move disk",n,"from source",source,"to destination",destination)
    
    new_state = copy.deepcopy(states[-1])
    new_state[source].pop()
    new_state[destination].append(n)
    states.append(new_state)

    # Move n-1 disks from auxiliary to destination using source as auxiliary
    solve_tower_of_hanoi(n-1, auxiliary, destination, source)
         
# Driver code
N = 3
states.append(
    {
        "A": [x for x in range(N,0,-1)],
        "B": [],
        "C": []
    }
)
solve_tower_of_hanoi(N,'A','C','B') 
# A, C, B are the name of rods


# Visualization
import compas.geometry as cg
from compas.colors import Color
from compas_view2.app import App

CYLINDER_RADIUS_STEP = 0.2
CYLINDER_INITIAL_RADIUS = 0.2
CYLINDER_HEIGHT = 0.3

viewer = App(enable_sidebar=True, show_grid=False)
rod_y_coords = {
    "A": (N+1) * CYLINDER_RADIUS_STEP * -2 - 0.1,
    "B": 0,
    "C": (N+1) * CYLINDER_RADIUS_STEP * 2 + 0.1
}

# Add rods
for value in rod_y_coords.values():
    line = cg.Line([0, value, 0], [0, value, (N+1)* CYLINDER_HEIGHT])
    viewer.add(line, linewidth=5)

# Add base
frame = cg.Frame([0, 0, -0.25], [1, 0, 0], [0, 1, 0])
box = cg.Box(frame, 3 * N * CYLINDER_RADIUS_STEP, 9 * N * CYLINDER_RADIUS_STEP, 0.5)
viewer.add(box, facecolor=Color(0.95, 0.95, 0.95))

cylinder_objs = []
for i in range(N):
    plane = cg.Plane([0, rod_y_coords['A'], (N-i-0.5) * CYLINDER_HEIGHT], [0,0,1])
    circle = cg.Circle(plane, CYLINDER_RADIUS_STEP*(i+1)+CYLINDER_INITIAL_RADIUS)
    cylinder = cg.Cylinder(circle, CYLINDER_HEIGHT)
    cylinder_obj = viewer.add(cylinder, facecolor=Color(1, 1-(i+1)/N, 1-(i+1)/N))
    cylinder_objs.append(cylinder_obj)

@viewer.slider(title="Slide Point", maxval=len(states)-1, step=1)
def slide(value):
    for key, _value in states[int(value)].items():
        for i, v in enumerate(_value):
            plane = cg.Plane([0, rod_y_coords[key], (i+0.5) * CYLINDER_HEIGHT], [0,0,1])
            circle = cg.Circle(plane, CYLINDER_RADIUS_STEP*v+CYLINDER_INITIAL_RADIUS)
            cylinder = cg.Cylinder(circle, CYLINDER_HEIGHT)
            cylinder_objs[v-1]._data = cylinder
            cylinder_objs[v-1].update()
    viewer.view.update()

viewer.run()