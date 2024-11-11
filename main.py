import numpy as np
import pygame
import pymunk

from src.genetic_algorithm import GeneticAlgorithm
from src.agent_parts.vision import Vision
from src.render_object import RenderObject
from src.interface import Button, Interface
from src.runner_display import display_genome_run
from src.agent_parts.limb import Limb
from src.globals import FONT_SIZE, SEGMENT_WIDTH, BLACK, RED
from src.agent_parts.rectangle import Point
from src.environment import Environment, GroundType
from src.agent_parts.creature import Creature
from src.NEATnetwork import NEATNetwork
from src.genome import Genome
from src.globals import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    POPULATION_SIZE,
    SPECIATION_THRESHOLD,
    NUM_GENERATIONS,
    SIMULATION_STEPS,
)


def evaluate_genome(genome: Genome) -> float:
    """Evaluate a genome by running a simulation and returning its fitness."""
    # Initialize Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 981)

    # Minimal screen for Pymunk (no rendering during evaluation)
    screen = pygame.Surface((1, 1))

    # Initialize environment
    environment = Environment(screen, space)
    environment.ground_type = GroundType.BASIC_GROUND

    # Instantiate NEATNetwork and Creature
    network = NEATNetwork(genome)
    vision = Vision(Point(0, 0))
    creature = Creature(space, vision)
    # Initialize creature's limbs and motors
    limb1 = creature.add_limb(100, 20, (300, 300), mass=1)
    limb2 = creature.add_limb(100, 20, (350, 300), mass=3)
    limb3 = creature.add_limb(80, 40, (400, 300), mass=5)
    creature.add_motor_on_limbs(limb1, limb2, (325, 300))
    creature.add_motor_on_limbs(limb2, limb3, (375, 300))

    # Run simulation for a certain number of steps
    for _ in range(SIMULATION_STEPS):
        inputs = []
        # Prepare inputs
        inputs.extend(
            [
                creature.vision.get_near_periphery().x,
                creature.vision.get_near_periphery().y,
                creature.vision.get_far_periphery().x,
                creature.vision.get_far_periphery().y,
            ]
        )
        inputs.extend(creature.get_joint_rates())
        for limb in creature.limbs:
            inputs.extend([limb.body.position.x, limb.body.position.y])

        # Ensure inputs match the expected number
        inputs = np.array(inputs)
        if len(inputs) != genome.num_inputs:
            # Handle input size mismatch if necessary
            # For simplicity, we'll pad with zeros or truncate
            if len(inputs) < genome.num_inputs:
                inputs = np.pad(
                    inputs, (0, genome.num_inputs - len(inputs)), "constant"
                )
            else:
                inputs = inputs[: genome.num_inputs]

        outputs = network.forward(inputs)
        creature.set_joint_rates(outputs)

        creature.vision.update(
            Point(creature.limbs[0].body.position.x, creature.limbs[0].body.position.y),
            environment.ground,
            environment.offset,
        )
        space.step(1 / 60.0)

    # Evaluate fitness (e.g., distance traveled)
    fitness = creature.limbs[0].body.position.x
    return fitness


def train() -> Genome:

    pygame.init()

    # Initialize a temporary creature to determine number of inputs and outputs
    temp_space = pymunk.Space()
    temp_space.gravity = (0, 981)
    temp_screen = pygame.Surface((1, 1))
    temp_environment = Environment(temp_screen, temp_space)
    temp_environment.ground_type = GroundType.BASIC_GROUND

    vision = Vision(Point(0, 0))
    temp_creature = Creature(space=temp_space, vision=vision)
    limb1 = temp_creature.add_limb(100, 20, (300, 300), mass=1)
    limb2 = temp_creature.add_limb(100, 20, (350, 300), mass=3)
    limb3 = temp_creature.add_limb(80, 40, (400, 300), mass=5)
    temp_creature.add_motor_on_limbs(limb1, limb2, (325, 300))
    temp_creature.add_motor_on_limbs(limb2, limb3, (375, 300))

    # Determine number of inputs and outputs
    amount_of_joints = temp_creature.get_amount_of_joints()
    amount_of_limb = temp_creature.get_amount_of_limb()
    num_inputs = 4 + amount_of_joints + (amount_of_limb * 2)
    num_outputs = amount_of_joints

    # Clean up temporary simulation
    del temp_creature
    del temp_space
    del temp_environment
    del temp_screen

    # Initialize a new Creature to pass as initial_creature
    # Since GeneticAlgorithm uses initial_creature to determine inputs and outputs,
    # we'll create a dummy creature without needing to initialize a full simulation
    dummy_space = pymunk.Space()
    dummy_space.gravity = (0, 981)
    dummy_vision = Vision(Point(0, 0))
    initial_creature = Creature(dummy_space, dummy_vision)

    limb1 = initial_creature.add_limb(100, 20, (300, 300), mass=1)
    limb2 = initial_creature.add_limb(100, 20, (350, 300), mass=3)
    limb3 = initial_creature.add_limb(80, 40, (400, 300), mass=5)
    initial_creature.add_motor_on_limbs(limb1, limb2, (325, 300))
    initial_creature.add_motor_on_limbs(limb2, limb3, (375, 300))

    # Initialize Genetic Algorithm with population size and initial creature
    ga = GeneticAlgorithm(
        population_size=POPULATION_SIZE,
        initial_creature=initial_creature,
        speciation_threshold=SPECIATION_THRESHOLD,
    )

    # Run Evolution
    ga.evolve(generations=NUM_GENERATIONS, evaluate_function=evaluate_genome)

    # After evolution, select the best genome
    best_genome = max(ga.population, key=lambda g: g.fitness, default=None)
    if best_genome:
        print("Best Genome:", best_genome)
    else:
        print("No genomes in population.")

    return best_genome


def main():

    best_genome = train()
    display_genome_run(best_genome)


if __name__ == "__main__":
    main()
