from environment import Environment
from renderObject import RenderObject
from agent_parts.rectangle import Rectangle
from enum import Enum
import numpy
import pygame


class LimbType(Enum):
    LIMB = 1
    HEAD = 2     
    FOOT = 3

class Limb(RenderObject):
    rect: Rectangle
    damage_scale: float 
    orientation: float
    
    def rotate(self, angle: float):
        self.orientation += angle
    
    def inherit_orientation(self, parent_orientation: float, limb_oreientation: float):
        self.orientation= parent_orientation  + limb_oreientation
        
    def __init__(self, rect: Rectangle, damage_scale: float, limbType: LimbType):
        self.rect = rect
        self.damage_scale = damage_scale
        self.limbType = limbType

    def updatePosition(self, x: float, y: float):
        self.rect.updatePosition(x, y)     

    def render(self,window):
        self.rect.render(window)
    
    def getAngle(self):
        return self.orientation

    def setAngle(self, angle: float):
        self.orientation = angle
    
    


def limb_factory(rect: Rectangle, limbType: LimbType, orientation: float) -> Limb:
    """
    Factory function for creating a limb object.
    """
    print()
    damage_scale: float = 0
    match limbType:
        case 1: damage_scale = 0.1
        case 2: damage_scale = 1
        case 3: damage_scale = 0
        case _:
            return "Invalid LimbType"
    
    return Limb(rect, damage_scale, orientation)




