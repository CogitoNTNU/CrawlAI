from typing import Protocol
from enum import Enum
import numpy
import random

import pygame
import pymunk
from pygame.locals import *

from src.genome import Genome
from src.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from src.environment import Environment, GroundType
from src.render_object import RenderObject


from src.agent_parts.creature import Creature

def main():
    # Initialize Pygame and Pymunk
    pygame.init()
    screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pymunk Rectangle Physics")

    environment = Environment(screen)
    environment.ground_type = GroundType.BASIC_GROUND

    if environment.ground_type == GroundType.BASIC_GROUND:
            environment.ground.generate_floor_segment(0)

    # Set up the Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 981)  # Gravity pointing downward

    creature = Creature(space)

    # Add limbs to the creature, placing them above the ground
    limb1 = creature.add_limb(100, 20, (300, 100), mass=1)  # Positioned above the ground
    limb2 = creature.add_limb(100, 20, (350, 100), mass=1)  # Positioned above the ground
    limb3 = creature.add_limb(110, 20, (400, 100), mass=5)

    # Add a motor between limbs
    creature.add_motor(limb1, limb2, (50, 0), (-25, 0), rate=2, tolerance=30)
    creature.add_motor(limb2, limb3, (37, 0), (-23, 0), rate=-2, tolerance=50)

    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("Left arrow pressed")
                if event.key == pygame.K_RIGHT:
                    print("Right arrow pressed")

        space.step(1/200.0)

        screen.fill((135, 206, 235))
        
        environment.update()
        environment.render()

        creature.set_joint_rates([random.random()*2, random.random()*2])
        # Render the creature
        creature.render(screen)
            
            
        clock.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()