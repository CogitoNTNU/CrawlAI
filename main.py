from typing import Protocol
from enum import Enum
import numpy

from src.genome import Genome
from src.environment import Environment
from CrawlAI.src.render_object import RenderObject

from src.agent_parts.limb import Limb, LimbType, limb_factory
from src.agent_parts.creature import Creature, creature_factory
from src.agent_parts.rectangle import Rectangle, rectangle_factory, Point
from src.agent_parts.joint import Joint, joint_factory

if __name__ =="__main__":
    import pygame

    GRAVITY = 9.81

    point = Point(100, 100)

    rect = rectangle_factory(point, 50, 50)
    limb = limb_factory(rect, 3, 2)
    angle = 0
    joint = joint_factory(angle, Point(125, 125))
    limb.addJoint(joint)
    aurelius = creature_factory(None, [limb])
    
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    active = True
    a = 0
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
        window.fill((0, 0, 0))
        pygame.draw.rect(window, (255, 0, 0), (0, 0, 800, 600))
        aurelius.render(window)
        a+= 0.001
        for limb in aurelius.limblist:
            limb.rotate(a)
        pygame.display.flip()
        pygame.time.delay(10)
        
        
    
    pygame.quit()