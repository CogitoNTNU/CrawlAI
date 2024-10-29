import pygame
import pymunk
from creature import Creature
from limb import Limb
import random

def create_ground(space, width, height, position=(0, 0)):
    """Create a static ground body to interact with the creature."""
    ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    ground_body.position = position
    ground_shape = pymunk.Segment(ground_body, (0, 0), (width, 0), height)
    ground_shape.friction = 1.0
    space.add(ground_body, ground_shape)
    return ground_shape


# Pygame and Pymunk setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create a Pymunk space for the simulation
space = pymunk.Space()
space.gravity = (0, 981)  # Gravity similar to Earth (in pixels/s²)

# Create the creature
creature = Creature(space)

# Add limbs to the creature, placing them above the ground
limb1 = creature.add_limb(100, 20, (300, 300), mass=1)  # Positioned above the ground
limb2 = creature.add_limb(100, 20, (350, 300), mass=1)  # Positioned above the ground
limb3 = creature.add_limb(110, 20, (400, 300), mass=5)

# Add a motor between limbs
creature.add_motor(limb1, limb2, (50, 0), (-25, 0), rate=2, tolerance= 30)
creature.add_motor(limb2, limb3, (37, 0), (-23, 0), rate=-2, tolerance= 50)
# Create the ground
ground = create_ground(space, width=800, height=10, position=(0, 550))

# Main loop
running = True
while running:
    screen.fill((255, 255, 255))

    # Update physics
    space.step(1/60.0)

    # Render the ground (draw as a line)
    pygame.draw.line(screen, (0, 0, 0), (0, 550), (800, 550), 10)

    print(creature.get_joint_rates())
    creature.set_joint_rates([random.random()*2, random.random()*2])
    # Render the creature
    creature.render(screen)

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()