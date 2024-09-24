from environment import Environment
from renderObject import RenderObject
from agent_parts.limb import Limb

class Joint(RenderObject):
    angle: float
    limb1: Limb
    limb2: Limb
    position1: list[float, float]
    position2: list[float, float]

    def __init__(self, angle: float, limb1: Limb, limb2: Limb, position1: list[float, float], position2: list[float, float]):
        self.angle = angle
        self.limb1 = limb1
        self.limb2 = limb2
        self.position1 = position1
        self.position2 = position2
    
    def render(self):
        pass

    def rotate(self, angle: float):
        self.angle += angle
        
    def get_angle(self):
        return self.angle
    
    def set_angle(self, angle: float):
        self.angle = angle


def joint_factory(parent: Limb, child: Limb) -> Joint:
    """
    Factory function for creating a joint object.
    """
    return Joint()