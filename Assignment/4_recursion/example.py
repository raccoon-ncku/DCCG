import random
import compas.geometry as cg
from compas_viewer import Viewer


def generate_branches(start, direction, length, depth):
    """Recursive function to generate tree branches.
    
    Parameters
    ----------
    start : Point
        The start point of the branch.
    direction : Vector
        The direction of the branch.
    length : float
        The length of the branch.
    depth : int
        The depth of the recursion.
    
    Returns
    -------
    list
        A list of Line objects representing the branches.    
    """
    
    # Base case: stop recursion and return an empty list
    if depth > MAX_DEPTH:
        return []
    else:
        # Recursive case: generate branches and return the current branch
        
        # Calculate the end point of the current branch
        end = start + direction * length

        # Create the current branch as a line segment
        branch = cg.Line(start, end)
        branches = [branch]

        # Generate child branches
        for _ in range(BRANCH_COUNT):
            # Randomly rotate the direction for child branches
            rotation = cg.Rotation.from_axis_and_angle((random.gauss(), random.gauss(), random.gauss()), ANGLE)
            new_direction = direction.transformed(rotation)

            branches += generate_branches(
                end,
                new_direction,
                length * 0.7,  # Reduce length for child branches
                depth + 1, # Increase depth for child branches, eventually reaching the base case
            )
        return branches


# Initial parameters
ROOT = cg.Point(0, 0, 0)
INITIAL_DIRECTION = cg.Vector(0, 0, 1)
INITIAL_LENGTH = 1.0
INITIAL_DEPTH = 0

# Recursion parameters
MAX_DEPTH = 4

# Branching parameters
ANGLE = 0.6 # in radians
BRANCH_COUNT = 3

# Generate tree geometry
tree_branches = generate_branches(ROOT, INITIAL_DIRECTION, INITIAL_LENGTH, INITIAL_DEPTH)

# Visualization
viewer = Viewer()
viewer.scene.add(tree_branches)
viewer.show()
