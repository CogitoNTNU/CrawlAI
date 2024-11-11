# main.py

import numpy as np
import pygame
from src.agent_parts.vision import Vision
from src.genetic_algorithm import GeneticAlgorithm
import pymunk

from src.agent_parts.vision import Vision
from src.agent_parts.limb import Limb
from src.genome import Genome
from src.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from src.environment import Environment, GroundType
from src.render_object import RenderObject
from src.interface import Button, Interface
from src.agent_parts.limb import Limb
from src.agent_parts.rectangle import Point
from src.agent_parts.rectangle import Point
from src.globals import FONT_SIZE, SEGMENT_WIDTH, BLACK, RED
from src.agent_parts.rectangle import Point
from src.environment import Environment, GroundType
from src.interface import Interface
from src.agent_parts.creature import Creature
from src.NEATnetwork import NEATNetwork
from src.genome import Genome
from src.globals import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_neural_network(genome: Genome, screen, position=(0, 0), size=(300, 300)):
    """
    Draws the neural network represented by the genome onto the Pygame screen.

    :param genome: The Genome object containing nodes and connections.
    :param screen: The Pygame surface to draw on.
    :param position: The (x, y) position of the top-left corner where to draw the network.
    :param size: The (width, height) size of the area to draw the network.
    """
    x, y = position
    width, height = size

    # Get nodes by type
    input_nodes = [node for node in genome.nodes if node.node_type == 'input']
    hidden_nodes = [node for node in genome.nodes if node.node_type == 'hidden']
    output_nodes = [node for node in genome.nodes if node.node_type == 'output']

    # Assign positions to nodes
    node_positions = {}

    # Vertical spacing
    layer_nodes = [input_nodes, hidden_nodes, output_nodes]
    max_layer_nodes = max(len(layer) for layer in layer_nodes)
    node_radius = 10
    vertical_spacing = height / (max_layer_nodes + 1)

    # Horizontal positions for layers
    num_layers = 3
    layer_x_positions = [x + width * i / (num_layers - 1) for i in range(num_layers)]

    # Position nodes in each layer
    for layer_idx, nodes in enumerate(layer_nodes):
        layer_x = layer_x_positions[layer_idx]
        num_nodes = len(nodes)
        for idx, node in enumerate(nodes):
            # Center nodes vertically
            node_y = y + (idx + 1) * height / (num_nodes + 1)
            node_positions[node.id] = (layer_x, node_y)

    # Draw connections
    for conn in genome.connections:
        if conn.enabled:
            in_pos = node_positions.get(conn.in_node)
            out_pos = node_positions.get(conn.out_node)
            if in_pos and out_pos:
                weight = conn.weight
                # Color code based on weight
                color = (0, 0, 255) if weight > 0 else (255, 0, 0)
                # Normalize weight for thickness
                thickness = max(1, int(abs(weight) * 2))
                pygame.draw.line(screen, color, in_pos, out_pos, thickness)

    # Draw nodes
    for node_id, pos in node_positions.items():
        node = next((n for n in genome.nodes if n.id == node_id), None)
        if node:
            if node.node_type == 'input':
                color = (0, 255, 0)  # Green
            elif node.node_type == 'output':
                color = (255, 165, 0)  # Orange
            else:
                color = (211, 211, 211)  # Light Gray
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), node_radius)
            pygame.draw.circle(screen, (0, 0, 0), (int(pos[0]), int(pos[1])), node_radius, 1)


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
    simulation_steps = 300  # Adjust as needed
    for _ in range(simulation_steps):
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


def main():
    # Initialize Pygame
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

    # Genetic Algorithm Parameters
    population_size = 100
    num_generations = 20
    speciation_threshold = 3.0

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
        population_size=population_size,
        initial_creature=initial_creature,
        speciation_threshold=speciation_threshold,
    )

    # Run Evolution
    ga.evolve(generations=num_generations, evaluate_function=evaluate_genome)

    # After evolution, select the best genome
    best_genome = max(ga.population, key=lambda g: g.fitness, default=None)
    if best_genome:
        print("Best Genome:", best_genome)
    else:
        print("No genomes in population.")

    # Initialize Pygame display for visualization
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("NEAT Simulation")
    clock = pygame.time.Clock()
    interface = Interface()

    # Initialize Pymunk space and environment for visualization
    space = pymunk.Space()
    space.gravity = (0, 981)
    environment = Environment(screen, space)
    environment.ground_type = GroundType.BASIC_GROUND

    # Population and creatures
    # population_size = 5
    # creature_population: list[Creature] = create_creatures(population_size, space)
    # creatures = creature_population.copy()
    # creature_instance: Creature = creatures[0]
    # population = create_population(population_size, creature_instance)
    # neat_networks: list[NEATNetwork] = []
    # for genome in population:
    #     neat_networks.append(NEATNetwork(genome))
    # Instantiate NEATNetwork and Creature with the best genome
    if best_genome:
        network = NEATNetwork(best_genome)
        vision = Vision(Point(0, 0))
        creature = Creature(space, vision)
        limb1 = creature.add_limb(100, 20, (300, 300), mass=1)
        limb2 = creature.add_limb(100, 20, (350, 300), mass=3)
        limb3 = creature.add_limb(80, 40, (400, 300), mass=5)

        # Add motors between limbs
        creature.add_motor_on_limbs(limb1, limb2, (325, 300))
        creature.add_motor_on_limbs(limb2, limb3, (375, 300))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            interface.handle_events(event)

        if best_genome:
            # Prepare inputs
            inputs = []
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
            if len(inputs) != best_genome.num_inputs:
                # Handle input size mismatch if necessary
                # For simplicity, we'll pad with zeros or truncate
                if len(inputs) < best_genome.num_inputs:
                    inputs = np.pad(
                        inputs, (0, best_genome.num_inputs - len(inputs)), "constant"
                    )
                else:
                    inputs = inputs[: best_genome.num_inputs]

            outputs = network.forward(inputs)
            creature.set_joint_rates(outputs)

            creature.vision.update(
                Point(
                    creature.limbs[0].body.position.x, creature.limbs[0].body.position.y
                ),
                environment.ground,
                environment.offset,
            )

        # Step the physics
        space.step(1 / 60.0)

        # Render everything
        screen.fill((135, 206, 235))
        environment.update()
        environment.render()
        if best_genome:
            creature.render(screen)
        
        network_position = (SCREEN_WIDTH - 350, 50)  
        network_size = (300, 300) 
        draw_neural_network(best_genome, screen, position=network_position, size=network_size)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
