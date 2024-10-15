from typing import Protocol
from enum import Enum
import numpy

import pygame
import pymunk
from pygame.locals import *

from src.genome import Genome
from src.environment import Environment
from src.renderObject import RenderObject

from src.agent_parts.limb import Limb, LimbType, limb_factory
from src.agent_parts.creature import Creature, creature_factory
from src.agent_parts.rectangle import Rectangle, rectangle_factory, Point
from src.agent_parts.joint import Joint, joint_factory

def main():
    # Initialize Pygame and Pymunk
    pygame.init()
    screen_width, screen_height = 800, 600
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pymunk Rectangle Physics")

    # Set up the Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 981)  # Gravity pointing downward

    # Create a rectangle and add its body and shape to the Pymunk space
    rect = rectangle_factory(Point(100, 100), 50, 20, 5.0)
    space.add(rect.body, rect.shape)

    static_rect = rectangle_factory(Point(140, 500), 300, 20, mass=0.0, body_type="static")  # No mass for static body
    space.add(static_rect.body, static_rect.shape)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Step the Pymunk simulation
        space.step(1 / 60.0)

        # Update the rectangle's position based on physics simulation
        rect.update_from_physics()
        static_rect.update_from_physics()

        # Clear the screen
        window.fill((0, 0, 0))

        # Render the rectangle
        rect.render(window)
        static_rect.render(window)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()