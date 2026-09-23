import random
from compas.geometry import Point, Translation, Circle, Frame

# Define the Agent class
class AgentBase:
    """
    Base class for agents in the model
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = Point(x, y, 0)

    def move(self):
        """
        Move the ant to a new location

        to work with the viewer, you need to update the body object using a transformation
        e.g. self.body.transform(translatoin)
        """

        raise NotImplementedError

    def set_viewer_obj(self, viewer_obj):
        """
        Set the viewer object for the agent.
        This is necessary for updating the agent's position in the compas_viewer.

        Parameters
        ----------
        viewer_obj : Viewer
            The viewer object
        """
        self.viewer_obj = viewer_obj

class Ant(AgentBase):
    """
    Class for an ant agent
    """

    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self):
        """
        Move the ant to a new location
        """
        raise NotImplementedError

class Obstacle:
    """
    Class for an obstacle agent
    """
    def __init__(self, x, y, radius):
        raise NotImplementedError

class AntAvoidObstacles(AgentBase):
    """
    Class for an ant agent that avoids obstacles
    """

    def __init__(self, x, y, obstacles):
        super().__init__(x, y)
        self.obstacles = obstacles

    def move(self):
        """
        Move the ant to a new location while avoiding obstacles
        """
        

        # Check if the new location is inside an obstacle
        # If the new location is inside an obstacle, don't move
        raise NotImplementedError