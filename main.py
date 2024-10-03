from typing import Protocol
from enum import Enum
import numpy

from src.genome import Genome
from src.environment import Environment
from src.renderObject import RenderObject

from src.agent_parts.limb import Limb, LimbType, limb_factory
from src.agent_parts.creature import Creature, creature_factory
from src.agent_parts.rectangle import Rectangle, rectangle_factory

if __name__ =="__main__":
    import pygame

    GRAVITY = 9.81


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
        for limb in aurelius.limblist:
            limb.rotate(0.1)
        pygame.display.flip()
        pygame.time.delay(10)
        
        
    
    pygame.quit()