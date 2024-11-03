from typing import Protocol
from enum import Enum
import numpy
import random

import pygame
from CrawlAI.src.genetic_algoritm import GeneticAlgorithm
import pymunk
from pygame.locals import *

from src.genome import Genome
from src.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from src.environment import Environment, GroundType
from src.agent_parts.rectangle import Point
from src.genetic_algoritm import GeneticAlgorithm
from src.globals import (
    FONT_SIZE,
    SEGMENT_WIDTH,
    BLACK,
    RED
    )
from src.agent_parts.creature import Creature
from src.NEATnetwork import NEATNetwork


def create_creatures(amount, space):
    creatures = []
    for i in range(amount):
        creature = Creature(space)
        # Add limbs to the creature, placing them above the ground
        limb1 = creature.add_limb(100, 60, (300, 100), mass=1)  
        limb2 = creature.add_limb(100, 20, (350, 100), mass=1)  
        limb3 = creature.add_limb(110, 60, (400, 100), mass=5)

        # Add a motor between limbs
        creature.add_motor(
            limb1, 
            limb2, 
            (50, 0), 
            (-25, 0), 
            rate=-2, tolerance=30)
        creature.add_motor(
            limb2, 
            limb3, 
            (37, 0), 
            (-23, 0), 
            rate=2, 
            tolerance=50)
        
        creatures.append(creature)
        
    return creatures

def create_population(population_size, creature: Creature):
    amount_of_joints = creature.get_amount_of_joints()
    amount_of_out_nodes = amount_of_joints
    # vision -> 4 nodes
    amount_of_in_nodes = 4
    # joint rates
    amount_of_in_nodes += amount_of_joints
    # limb positions
    amount_of_in_nodes += creature.get_amount_of_limb() * 2
    
    population = GeneticAlgorithm.initialize_population(population_size, amount_of_in_nodes, amount_of_out_nodes)

    return population 

def main():


    #Initializes Genetic Algorithm 

    genetic_algorithm = GeneticAlgorithm()

    def create_creature(in_nodes: int,out_nodes: int):
        population = genetic_algorithm.initialize_population(200, in_nodes, out_nodes)

        return population 

    fitness = []

    # Initialize Pygame and Pymunk
    
    pygame.init()
    screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pymunk Rectangle Physics")
            
    space = pymunk.Space()
    space.gravity = (0, 981)  # Gravity pointing downward

    environment = Environment(screen, space)
    environment.ground_type = GroundType.BASIC_GROUND

    population_size = 10
    creatures = create_creatures(population_size, space)
    population = create_population(population_size, creatures[0])
    
    clock = pygame.time.Clock()
    vision_y = 100
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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

        vision_y += random.randint(-1, 1)

        match environment.ground_type:
            case GroundType.BASIC_GROUND:
                environment.vision.update(
                    environment.screen,
                    Point(environment.starting_xx, vision_y),
                    environment.ground,
                    environment.offset)

            case GroundType.PERLIN:
                environment.vision.update(
                    screen,
                    Point(environment.starting_xx, vision_y),
                    environment.ground,
                    0)

        #creature.set_joint_rates([random.random()*2, random.random()*2])
        # Render the creature
        creature.render(screen)
        
            
            
        clock.tick(60)

        pygame.display.flip()


    pygame.quit()








if __name__ == "__main__":
    main()