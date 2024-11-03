from typing import Protocol
from enum import Enum
import numpy
import random

import pygame
from src.genetic_algoritm import GeneticAlgorithm
import pymunk
from pygame.locals import *

from src.genome import Genome
from src.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from src.environment import Environment, GroundType
from src.render_object import RenderObject
from src.agent_parts.rectangle import Point
from src.globals import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FONT_SIZE,
    SEGMENT_WIDTH,
    BLACK,
    RED
    )


from src.agent_parts.creature import Creature

def main():
    # Initialize Pygame and Pymunk
    pygame.init()
    screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pymunk Rectangle Physics")
            

    # Set up the Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 981)  # Gravity pointing downward


    environment = Environment(screen, space)
    environment.ground_type = GroundType.BASIC_GROUND

    population_size = 10
    creatures = create_creatures(population_size, space)
    creature_instance = creatures[0]
    population = create_population(population_size, creature_instance)
    
    clock = pygame.time.Clock()
    vision_y = 100
    vision_x = 0
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

        space.step(1/60.0)

        screen.fill((135, 206, 235))
        
        environment.update()
        environment.render()
        
        import numpy as np
        # TODO: vision should be part of a creature, and not environment
        inputs = np.array([environment.vision.near_periphery.x, 
                           environment.vision.near_periphery.y, 
                           environment.vision.far_periphery.x, 
                           environment.vision.far_periphery.y])
        for index, creature in enumerate(creatures):
            network = population[index]
            for joint_rate in creature.get_joint_rates():
                inputs = np.append(inputs, joint_rate)
            
            for
            
            
            

        vision_y = round(creature_instance.limbs[0].body.position.y)
        vision_x = round(creature_instance.limbs[0].body.position.x)

        match environment.ground_type:
            case GroundType.BASIC_GROUND:
                environment.vision.update(
                    environment.screen,
                    Point(vision_x, vision_y),
                    environment.ground,
                    environment.offset)

            case GroundType.PERLIN:
                environment.vision.update(
                    environment.screen,
                    Point(vision_x, vision_y),
                    environment.ground,
                    0)
   
        creature_instance.render(screen)
            
        clock.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
    # pygame.init()
    # font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)

    # space = pymunk.Space()
    # space.gravity = (0, 981)  # Gravity pointing downward

    # # Create the screen
    # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # environment = Environment(screen, space)
    # # Start the main loop
    # environment.run()