from typing import List
from enviroment import Enviroment
from renderObject import RenderObject
from agent import Agent
from limb import Limb
from joint import Joint

class Creature(RenderObject):
    _limbs: list
    _joints: list  
    
    
    def __init__(self, env):
        self.env = env
    
    def render(self):
        pass

def creature_factory(env: Enviroment, limblist: list, jointlist: list):
    """
    Factory function for creating a creature object.
    """
    return Creature(env)