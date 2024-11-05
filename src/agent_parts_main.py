from typing import Protocol
from enum import Enum
import numpy
import random

import pygame
import pymunk
from pygame.locals import *

from genome import Genome
from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from environment import Environment, GroundType
from render_object import RenderObject
from interface import Button, Interface
from agent_parts.limb import Limb
from ground import *

from agent_parts.creature import Creature

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
    
    def handle_physics():
        nonlocal physics_on
        nonlocal physics_value
        physics_value = 1/60.0 if physics_value == 0 else 0
        physics_on = True if physics_value != 0 else False
        print("Physics Enabled" if physics_value != 0 else "Physics Disabled")

    font = pygame.font.Font(None, 20)

    pause_button = Button(
        text="Pause",
        pos=(10, 10),
        width=100,
        height=30,
        font=font,
        color=(70, 130, 180),
        hover_color=(100, 149, 237),
        text_color=(255, 255, 255),
        active_color=(200, 100, 100),
        callback=handle_physics
    )

    make_limb_mode = False

    def make_limb():
        nonlocal make_limb_mode
        make_limb_mode = not make_limb_mode

    limb_button = Button(
        text="Add limb",
        pos=(10, 50),
        width=100,
        height=30,
        font=font,
        color=(70, 130, 180),
        hover_color=(100, 149, 237),
        text_color=(255, 255, 255),
        active_color=(200, 100, 100),
        callback=make_limb
    )

    interface.add_button(pause_button)



    # Set up the Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 981)  # Gravity pointing downward

    environment = Environment(screen, space)
    environment.ground_type = GroundType.BASIC_GROUND


    creature = Creature(space)

    # Add limbs to the creature, placing them above the ground
    #limb1 = creature.add_limb(100, 20, (300, 100), mass=1)  # Positioned above the ground
    #limb2 = creature.add_limb(100, 20, (350, 100), mass=1)  # Positioned above the ground
    #limb3 = creature.add_limb(110, 20, (400, 100), mass=5)

    # Add a motor between limbs
    #creature.add_motor(limb1, limb2, (50, 0), (-25, 0), rate=2, tolerance=30)
    #creature.add_motor(limb2, limb3, (37, 0), (-23, 0), rate=-2, tolerance=50)

    # Add limbs to the creature
    limb1 = creature.add_limb(100, 20, (300, 300), mass=1)
    limb2 = creature.add_limb(100, 20, (350, 300), mass=3)
    limb3 = creature.add_limb(80, 40, (400, 300), mass=5)

    # Add motors between limbs
    #creature.add_motor(limb1, limb2, (25, 0), (-25, 0), rate=2)
    #creature.add_motor(limb2, limb3, (37, 0), (-23, 0), rate=-2)
    creature.add_motor_on_limbs(limb1, limb2, (325, 300))
    creature.add_motor_on_limbs(limb2, limb3, (375, 300))

    #dragging creature properties 
    dragging = False
    dragged_limb = None
    drag_offset = []

    # creating rectangles properties
    start_pos = None 
    end_pos = None
    limbs = []

    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            interface.handle_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("Left arrow pressed")
                if event.key == pygame.K_RIGHT:
                    print("Right arrow pressed")
                if event.key == pygame.K_SPACE:
                    handle_physics()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not physics_on:
                    mouse_x, mouse_y = event.pos
                    mouse_pos = (mouse_x, mouse_y)
                    # For dragging creature: Check if the mouse is over any limb
                    if not make_limb_mode:
                        for limb in creature.limbs: 
                            if limb.contains_point(mouse_pos):
                                dragging = True 
                                dragged_limb = limb 
                                creature.start_dragging(dragged_limb)
                                drag_offset = (limb.body.position.x - mouse_x, limb.body.position.y - mouse_y)
                                break
                    # For creating rectangles
                    elif make_limb_mode:
                        start_pos = mouse_pos

            elif event.type == MOUSEMOTION and make_limb_mode:
                mouse_x, mouse_y = event.pos
                mouse_pos = (mouse_x, mouse_y)
                end_pos = mouse_pos

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                if make_limb_mode and start_pos and end_pos:
                    width = abs(start_pos[0] - end_pos[0])
                    height = abs(start_pos[1] - end_pos[1])
                    position = ((start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2)
                    limb = creature.add_limb(width, height, position)

                # Reset start and end positions
                start_pos = None
                end_pos = None


        space.step(physics_value)   

        if dragging and dragged_limb and not make_limb_mode:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            new_position = (mouse_x + drag_offset[0], mouse_y + drag_offset[1])
            creature.update_creature_position(dragged_limb, new_position)

        screen.fill((135, 206, 235))
        environment.update()
        environment.render()

        #creature.set_joint_rates([random.random()*2, random.random()*2])
        # Render the creature
        creature.render(screen)
        
        if not physics_on: 
            interface.add_button(limb_button)
        else: 
            interface.remove_button(limb_button)
        interface.render(screen)

      
            
        clock.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()