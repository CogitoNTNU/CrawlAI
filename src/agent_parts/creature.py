from typing import List
from environment import Environment
from renderObject import RenderObject
from agent_parts.limb import Limb
from agent_parts.joint import Joint
# from joint import Joint

class Creature:
    """
    A class representing a creature composed of limbs and joints in a given environment.

    Attributes:
    ----------
    env : Environment
        The environment in which the creature exists.
    limblist : list[Limb]
        A list of Limb objects representing the creature's limbs.
    jointlist : list[Joint]
        A list of Joint objects representing the creature's joints.
    position : list[float, float]
        The position of the creature represented as a list containing two floats [x, y].
    """
    
    env: Environment
    limblist: list[Limb]
    jointlist: list[Joint]
    position: list[float, float]

    def __init__(self, env: Environment, limblist: list[Limb], jointlist: list[Joint]):
        """
        Initializes the Creature object.

        Parameters:
        ----------
        env : Environment
            The environment where the creature is situated.
        limblist : list[Limb]
            A list of Limb objects which form the creature.
        jointlist : list[Joint]
            A list of Joint objects which connect the limbs of the creature.

        The creature's initial position is set to [200, 200].
        """
        self.env = env
        self.limblist = limblist
        self.jointlist = jointlist
        self.position = [200, 200]
        
    def act(self, actions: list) -> None:
        """_summary_ Act on the environment based on the actions. This will rotate the joints. Creature physics must handle the rest.

        Args:
            actions (list): list of rotations for each joint.
        """
        for i in range(len(actions)):
            self.jointlist[i].rotate(actions[i])
    
    def render(self, window):
        """
        Renders the creature on a given window.

        Parameters:
        ----------
        window : any
            The graphical window where the creature will be rendered. 
            This can be any object capable of rendering the limbs and joints (e.g., a game screen or canvas).

        The function iterates through all the creature's limbs and joints and calls their respective render method.
        """
        for limb in self.limblist:
            print(limb)
            limb.render(window)
        for joint in self.jointlist:
            joint.render(window)
    
    def updatePosition(self, x: float, y: float):
        """
        Updates the creature's position and propagates the change to all its limbs.

        Parameters:
        ----------
        x : float
            The new x-coordinate of the creature.
        y : float
            The new y-coordinate of the creature.

        This method sets the new position of the creature and then updates the position of all limbs accordingly.
        """
        self.position = [x, y]
        for limb in self.limblist:
            limb.updatePosition(x, y)

def creature_factory(env: Environment, limblist: list[Limb], jointlist: list[Joint]) -> Creature:
    """
    Factory function for creating a Creature object.

    Parameters:
    ----------
    env : Environment
        The environment in which the creature will be created.
    limblist : list[Limb]
        A list of Limb objects to form the creature.
    jointlist : list[Joint]
        A list of Joint objects to connect the limbs of the creature.

    Returns:
    -------
    Creature:
        A new instance of the Creature class.
    """
    return Creature(env, limblist, jointlist)
