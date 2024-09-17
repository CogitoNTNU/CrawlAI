from enviroment import Enviroment
from renderObject import RenderObject
from creature import Creature
from rectangle import Rectangle
from enum import Enum


class LimbType(Enum):
    LIMB = 1
    HEAD = 2     
    FOOT = 3


class Limb(RenderObject):
    length: float
    width: float
    damage_scale: float 
    orientation: float
    
    def __init__(self, rect: Rectangle, damage_scale: float):
        self.rect = rect
        self.damage_scale = damage_scale
    
    def rotate(self, angle: float):
        self.orientation += angle
    
    def inherit_orientation(self, parent_orientation: float, limb_oreientation: float):
        self.orientation= parent_orientation  + limb_oreientation
        
        
        
    def render(self):
        #TODO: Implement render method
        pass
    
    def getAngle():
        #Returns a limbs angle in radians 

    def setAngle():

    
    


def limb_factory(rect: Rectangle, limbType: LimbType, orientation: float) -> Limb:
    """
    Factory function for creating a limb object.
    """
    damage_scale: float = 0
    match limbType:
        case 1: damage_scale = 0.1
        case 2: damage_scale = 1
        case 3: damage_scale = 0
        case _:
            return "Invalid LimbType"
    
    
    
    limb = Limb(rect, damage_scale, orientation)
    return Limb()




