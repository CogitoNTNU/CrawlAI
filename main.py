from typing import Protocol
from enum import Enum
import numpy
import random
import numpy as np
import pygame
from src.agent_parts.vision import Vision
from src.genetic_algoritm import GeneticAlgorithm
import pymunk
from pygame.locals import *

from src.agent_parts.limb import Limb
from src.genome import Genome
from src.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from src.environment import Environment, GroundType
from src.render_object import RenderObject
from src.interface import Button, Interface
from src.agent_parts.limb import Limb
from src.agent_parts.rectangle import Point


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
        vision = Vision(Point(0, 0))
        creature: Creature = Creature(space, vision)
        # Add limbs to the creature, placing them above the ground
        # limb1 = creature.add_limb(100, 60, (300, 100), mass=1)  
        # limb2 = creature.add_limb(100, 20, (350, 100), mass=3)  
        # limb3 = creature.add_limb(110, 60, (400, 100), mass=5)
        
        limb1 = creature.add_limb(100, 20, (300, 300), mass=1)
        limb2 = creature.add_limb(100, 20, (350, 300), mass=3)
        limb3 = creature.add_limb(80, 40, (400, 300), mass=5)

        # Add a motor between limbs
        creature.add_motor(
            limb1, 
            limb2, 
            (50, 0), 
            (-25, 0), 
            rate=0, tolerance=30)
        creature.add_motor(
            limb2, 
            limb3, 
            (37, 0), 
            (-23, 0), 
            rate=0, 
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


def apply_mutations(self):
    """
    Apply mutations to the genome based on defined mutation rates.
    """

    MUTATION_RATE_WEIGHT = 0.8  # 80% chance to mutate weights
    MUTATION_RATE_CONNECTION = 0.05  # 5% chance to add a new connection
    MUTATION_RATE_NODE = 0.03  # 3% chance to add a new node


    # Mutate weights with a certain probability
    if random.random() < MUTATION_RATE_WEIGHT:
        self.mutate_weights(delta=0.1)  # Adjust delta as needed

    # Mutate connections with a certain probability
    if random.random() < MUTATION_RATE_CONNECTION:
        self.mutate_connections()

    # Mutate nodes with a certain probability
    if random.random() < MUTATION_RATE_NODE:
        self.mutate_nodes()


def main():

    # Initialize Pygame and Pymunk
    pygame.init()
    screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pymunk Rectangle Physics")
    interface = Interface()
    
    # Track whether physics is on or off
    physics_on = False
    physics_value = 0
    
    # Set up the Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 981)  # Gravity pointing downward

    environment: Environment = Environment(screen, space)
    environment.ground_type = GroundType.BASIC_GROUND

    #Population and creatures
    population_size = 5
    creatures: list[Creature] = create_creatures(population_size, space)
    creature_instance: Creature = creatures[0]
    population = create_population(population_size, creature_instance)
    neat_networks: list[NEATNetwork] = []
    for genome in population:
        neat_networks.append(NEATNetwork(genome))
    
    clock = pygame.time.Clock()
    vision_y = 100
    vision_x = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            interface.handle_events(event)

        space.step(1/60.0)
        screen.fill((135, 206, 235))
        environment.update()
        environment.render()
        
        for index, creature in enumerate(creatures):
            inputs = np.array([creature.vision.get_near_periphery().x, 
                           creature.vision.get_near_periphery().y,
                           creature.vision.get_far_periphery().x,
                           creature.vision.get_far_periphery().y])
            network = population[index]
            for joint_rate in creature.get_joint_rates():
                inputs = np.append(inputs, joint_rate)
            
            for limb in creature.limbs:
                inputs = np.append(inputs, limb.body.position.x)
                inputs = np.append(inputs, limb.body.position.y)

            outputs = neat_networks[index].forward(inputs)
            creature.set_joint_rates(outputs)

            vision_y = round(creature.limbs[0].body.position.y)
            vision_x = round(creature.limbs[0].body.position.x)
            creature.vision.update(
                Point(vision_x, vision_y),
                environment.ground,
                environment.offset) # if perlin, offset = 0, if basic, offset = environment.offset

        #creature_instance.render(screen)
        for creature in creatures:
            creature.render(screen)
            
        clock.tick(60)

        pygame.display.flip()


    pygame.quit()




if __name__ == "__main__":
    main()
    

