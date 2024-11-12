import numpy as np
import pygame
import pymunk
import os
from src.genetic_algorithm import GeneticAlgorithm
from src.agent_parts.vision import Vision
from src.render_object import RenderObject
from src.interface import Button, Interface
from src.agent_parts.limb import Limb
from src.globals import FONT_SIZE, SEGMENT_WIDTH, BLACK, RED
from src.agent_parts.rectangle import Point
from src.environment import Environment, GroundType
from src.agent_parts.creature import Creature
from src.NEATnetwork import NEATNetwork
from src.genome import Genome
from src.interface import Button
from pygame_widgets.dropdown import Dropdown
import pygame_widgets
from src.globals import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    POPULATION_SIZE,
    SPECIATION_THRESHOLD,
    NUM_GENERATIONS,
    SIMULATION_STEPS,
)


def get_saved_file_paths() -> list[str]:
    """
    Returns a list of paths to saved genome files.
    """
    return [
        os.path.join("models/", f) for f in os.listdir("models/") if f.endswith(".json")
    ]


def display_genome_run(genome: Genome):
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
    font = pygame.font.Font(None, 20)
    train_enabled = False
    display_dropdown = False

    save_button = Button(
        pos=(10, SCREEN_HEIGHT - 100),
        width=80,
        height=40,
        color=(0, 200, 0),
        text="Save",
        text_color=(255, 255, 255),
        hover_color=(0, 255, 0),
        active_color=(0, 100, 0),
        font=font,
        callback=lambda: print("Load button clicked"),
    )

    train_button = Button(
        pos=(10, SCREEN_HEIGHT - 150),
        width=80,
        height=40,
        color=(0, 200, 0),
        text="Train",
        text_color=(255, 255, 255),
        hover_color=(0, 255, 0),
        active_color=(0, 100, 0),
        font=font,
        callback=lambda: (train_enabled := True),
    )
    interface.add_button(save_button)
    interface.add_button(train_button)

    choices = get_saved_file_paths()
    dropdown = Dropdown(
        screen,
        120,
        10,
        100,
        50,
        name="Load Genome",
        choices=choices,
        borderRadius=3,
        colour=pygame.Color("green"),
        values=choices,
        direction="down",
        textHAlign="left",
    )

    if genome:
        network = NEATNetwork(genome)
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
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            interface.handle_events(event)

        if genome:
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
                Point(
                    creature.limbs[0].body.position.x, creature.limbs[0].body.position.y
                ),
                environment.ground,
                environment.offset,
            )

        # Step the physics
        space.step(1 / 60.0)

        # Move all the bodies in the space as much as the creature has moved
        for body in space.bodies:
            creature_offset = creature.limbs[0].body.position.x
            body.position = (body.position.x - creature_offset / 100, body.position.y)

        # Render everything
        screen.fill((135, 206, 235))
        environment.update()
        environment.render()
        interface.render(screen)
        pygame_widgets.update(events)

        if genome:
            creature.render(screen)

        network_position = (SCREEN_WIDTH - 350, 50)
        network_size = (300, 300)
        draw_neural_network(
            genome, screen, position=network_position, size=network_size
        )
        # Add text with the fitness value and current x position
        font = pygame.font.Font(None, FONT_SIZE)
        fitness_text = font.render(f"Fitness: {genome.fitness:.2f}", True, BLACK)
        x_pos_text = font.render(
            f"X Position: {creature.limbs[0].body.position.x:.2f}", True, BLACK
        )
        screen.blit(fitness_text, (10, 10))
        screen.blit(x_pos_text, (10, 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


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
    input_nodes = [node for node in genome.nodes if node.node_type == "input"]
    hidden_nodes = [node for node in genome.nodes if node.node_type == "hidden"]
    output_nodes = [node for node in genome.nodes if node.node_type == "output"]

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
            if node.node_type == "input":
                color = (0, 255, 0)  # Green
            elif node.node_type == "output":
                color = (255, 165, 0)  # Orange
            else:
                color = (211, 211, 211)  # Light Gray
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), node_radius)
            pygame.draw.circle(
                screen, (0, 0, 0), (int(pos[0]), int(pos[1])), node_radius, 1
            )
