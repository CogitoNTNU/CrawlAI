from enviroment import Enviroment
from renderObject import RenderObject
from creature import Creature



class Limb():
    length: float
    width: float
    
    def __init__(self):
        pass

def limb_factory(lenght: float, width: float) -> Limb:
    """
    Factory function for creating a limb object.
    """
    return Limb()