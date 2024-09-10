from enviroment import Enviroment
from renderObject import RenderObject
from limb import Limb

class Joint():
    angle: float
    limb1: Limb
    limb2: Limb
    
    def __init__(self):
        pass

def joint_factory() -> Joint:
    """
    Factory function for creating a joint object.
    """
    return Joint()