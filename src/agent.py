from typing import Protocol
from enviroment import Enviroment
from renderObject import RenderObject
from enum import Enum
import pybox2d

class LimbType(Enum):  
    FOOT = 1
    LEG = 2
    LIMB = 3


class Agent(Protocol):
    def act(self, env) -> int:
        pass

    def save(self, path) -> None:
        pass

    def load(self, path) -> None:
        pass

    def get_genome(self) :
        pass



class Limb():
    
    def __init__(self, length: float, width: float, limbType: LimbType):
        self.length = length
        self.width = width
        self.limbType = limbType

    def render(self,window, x, y):
        pygame.draw.polygon(window, (255, 255, 255), ((x,y), (x+self.length,y), (x+self.length, y+self.width), (x, y+self.width)))

def limb_factory(length: float, width: float, limbType: LimbType) -> Limb:
    """
    Factory function for creating a limb object.
    """

    return Limb(length, width, limbType)

class Joint():
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

def joint_factory() -> Joint:
    """
    Factory function for creating a joint object.
    """
    return Joint()

class Creature():
    env: Enviroment
    limblist: list[Limb]
    jointlist: list[Joint]
    position: list[float, float]

    def __init__(self, env, limblist: list[Limb], jointlist: list[Joint]):
        self.env = env
        self.limblist = limblist
        self.jointlist = jointlist
        self.position = [200, 200]
    
    def render(self, window):
        self.limblist[0].render(window, self.position[0], self.position[1])

def creature_factory(env: Enviroment, limblist: list[Limb], jointlist: list[Joint]) -> Agent:
    """
    Factory function for creating a creature object.
    """

    return Creature(env, limblist, jointlist)

if __name__ =="__main__":
    import pygame

    limb = limb_factory(100, 70, LimbType.FOOT)

    aurelius = creature_factory(None, [limb], [])
    
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
        window.fill((0, 0, 0))
        pygame.draw.rect(window, (255, 0, 0), (0, 0, 800, 600))
        aurelius.render(window)
        pygame.display.flip()
        pygame.time.delay(10)
        
        
    
    pygame.quit()

    
    