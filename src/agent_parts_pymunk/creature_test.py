import pygame
import pymunk
from creature import Creature
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def create_ground(space, width, height, position=(0, 0)):
    """Create a static ground body to interact with the creature."""
    ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    ground_body.position = position
    ground_shape = pymunk.Segment(ground_body, (0, 0), (width, 0), height)
    ground_shape.friction = 1.0
    space.add(ground_body, ground_shape)
    return ground_shape

def setup_pygame():
    """Initialize Pygame screen and clock."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    return screen, clock

def setup_pymunk():
    """Initialize a Pymunk space with Earth-like gravity."""
    space = pymunk.Space()
    space.gravity = (0, 981)
    return space

def create_simulation(space):
    """Initialize the creature and its environment in the space."""
    creature = Creature(space)

    # Add limbs to the creature
    limb1 = creature.add_limb(100, 20, (300, 300), mass=1)
    limb2 = creature.add_limb(100, 20, (350, 300), mass=1)
    limb3 = creature.add_limb(80, 40, (400, 300), mass=5)

    # Add motors between limbs
    creature.add_motor(limb1, limb2, (25, 0), (-25, 0), rate=2)
    creature.add_motor(limb2, limb3, (37, 0), (-23, 0), rate=-2)

    # Create the ground in the space
    create_ground(space, width=800, height=10, position=(0, 550))
    return creature

def main_loop(screen, clock, space, creature, fps=60):
    """Runs the main simulation loop for rendering and updating the creature."""
    running = True
    ground_position = (0, 550)
    while running:
        screen.fill((255, 255, 255))

        # Update the physics simulation
        space.step(1 / fps)

        # Render the ground as a line
        pygame.draw.line(screen, (0, 0, 0), (0, ground_position[1]), (800, ground_position[1]), 10)

        current_joint_rates = creature.get_joint_rates()
        creature.set_joint_rates([random.uniform(0, 2) for _ in current_joint_rates])

        creature.render(screen)

        pygame.display.flip()
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

def run_simulation(simulation_id, frames=600):
    """Run a single simulation of the creature for a set number of frames."""
    screen, clock = setup_pygame()
    space = setup_pymunk()

    running = True
    for _ in range(frames):
        creature = create_simulation(space)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break  # Exit the event loop

        if not running:
            break  # Exit the main loop

        screen.fill((255, 255, 255))
        space.step(1 / 60.0)  # Update physics
        creature.set_joint_rates([random.uniform(0, 2) for _ in creature.get_joint_rates()])
        creature.render(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return simulation_id


def run_multiple_simulations(num_simulations=100, frames_per_simulation=200):
    """Run multiple simulations sequentially and collect results."""
    results = []
    for i in range(num_simulations):
        result = run_simulation(i, frames_per_simulation)
        results.append(result)
    return results

# Execute simulations
if __name__ == "__main__":
    space = setup_pymunk()
    screen, clock = setup_pygame()
    creature = create_simulation(space)
    main_loop(screen, clock, space, creature)

    # Run batch simulations
    results = run_multiple_simulations(num_simulations=100, frames_per_simulation=600)
    print("All simulations completed:", results)
