from typing import Protocol
from environment import Environment
from renderObject import RenderObject
from enum import Enum
from agent_parts.limb import Limb, LimbType, limb_factory
from agent_parts.creature import creature_factory
from agent_parts.rectangle import Rectangle, rectangle_factory
import numpy





GRAVITY = 9.81



class Agent(Protocol):
    def act(self, env) -> int:
        pass

    def save(self, path) -> None:
        pass

    def load(self, path) -> None:
        pass

    def get_genome(self) :
        pass


if __name__ =="__main__":
    import pygame


    rect = rectangle_factory(100, 100, 50, 50)
    limb = limb_factory(rect, 3, 2)

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
        aurelius.updatePosition(0, -GRAVITY)
        pygame.display.flip()
        pygame.time.delay(10)
        
        
    
    pygame.quit()

    
    