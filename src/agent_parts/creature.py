from typing import List
from environment import Environment
from renderObject import RenderObject
from agent_parts.limb import Limb
from agent_parts.joint import Joint
# from joint import Joint

class Creature():
    env: Environment
    limblist: list[Limb]
    jointlist: list[Joint]
    position: list[float, float]

    def __init__(self, env, limblist: list[Limb], jointlist: list[Joint]):
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
        for limb in self.limblist:
            print(limb)
            limb.render(window)
        for joint in self.jointlist:
            joint.render(window)
    
    def updatePosition(self, x: float, y: float):
        self.position = [x, y]
        for limb in self.limblist:
            limb.updatePosition(x, y)

def creature_factory(env: Environment, limblist: list[Limb], jointlist: list[Joint]) ->Creature:
    """
    Factory function for creating a creature object.
    """

    return Creature(env, limblist, jointlist)