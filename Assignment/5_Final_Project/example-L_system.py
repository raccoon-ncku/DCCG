# This is a example of how to implement a L-system in Python.

import compas.geometry as cg
from compas_view2.app import App
from math import cos, sin, radians
# The window
viewer = App()
FRAMERATE = 60
MAX_FRAME = 10000

# The pen (turtle)
x, y = 0, 0 # Initial position
angle = 0 # Initial angle
STEP = 10 # Distance to move forward
ANGLE = 90 # Angle to turn left or right

# The L-system
the_string = "A" # The axiom
num_loops = 4 # The number of times to apply the rules
the_rules = [] # array for rules
the_rules.append(['A', '-BF+CFA+FB-'])  #  first rule
the_rules.append(['B', '+A-FBFC-FA+'])  #  second rule
the_rules.append(['C', '+AF+CFB-FA-']) 

where_in_string = 0 # where in the L-system are we?

def lindenmayer(s):
    """interpret an L-system"""

    output = "" # start a blank output string
    for i in range(len(s)) :
        is_match = False # by default, no match
        for j in range(len(the_rules)):
            if s[i] == the_rules[j][0]: 
                output += the_rules[j][1] # write substitution
                is_match = True #  we have a match, so don't copy over symbol
                break  # get outta this for() loop

    # if nothing matches, just copy the symbol over.
    if not is_match: output += s[i]

    return output

def draw(k):
    """
    draw turtle graphics
    """
    global x, y, angle

    if k=='F':  # draw forward
        # polar to cartesian based on step and currentangle:
        x1 = x + STEP*cos(radians(angle))
        y1 = y + STEP*sin(radians(angle))
        viewer.add(cg.Line((x, y, 0), (x1, y1, 0))) # connect the old and the new
        # update the turtle's position:
        x = x1
        y = y1
    elif k == '+':
        angle += ANGLE # turn left
    elif k == '-':
        angle -= ANGLE # turn right
  
# Set up the scene
for i in range(num_loops):
    the_string += lindenmayer(the_string)

@viewer.on(interval=1000 / FRAMERATE, frames=MAX_FRAME)
def update(f):
    global where_in_string, the_string
    # draw the current character in the string:
    draw(the_string[where_in_string])
    
    # increment the point for where we're reading the string.
    # wrap around at the end.
    where_in_string += 1
    if where_in_string > len(the_string) -1:
       where_in_string = 0
print(the_string)
viewer.run()