from enviroment import Enviroment
from renderObject import RenderObject
from limb import Limb

class Joint():
    _angle: float
    _limb1: Limb
    _limb2: Limb
    
    
    def __init__(self):
        pass
    
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