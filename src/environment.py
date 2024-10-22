import pygame as pg
import random

import itertools
from enum import Enum

from ground import Ground, BasicGround, InterpolationType, PerlinNoise
from render_object import RenderObject
from agent_parts.rectangle import Point
from globals import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FONT_SIZE,
    SEGMENT_WIDTH,
    BLACK,
    RED
    )


pg.init()
font = pg.font.Font(pg.font.get_default_font(), FONT_SIZE)


# Remove this
interp_iter = itertools.cycle((
    InterpolationType.LINEAR, 
    InterpolationType.CUBIC, 
    InterpolationType.COSINE))

# Create the screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class GroundType(Enum):
    BASIC_GROUND = 1
    PERLIN = 2

    
class Environment(RenderObject):
    def __init__(self,  screen):
        self.screen = screen
        self.ground_type = GroundType.BASIC_GROUND
        self.ground: Ground = self.ground_factory(self.ground_type)
        self.starting_xx = 50
        self.point = Point(self.starting_xx, 300)
        self.vision: Vision = Vision(self.point)
        # TODO: change all references to noise to ground
        
        self.offset = 0
        self.offset_speed = 1
        
    def ground_factory(self, ground_type: GroundType) -> Ground:
        
        match ground_type:
            case GroundType.BASIC_GROUND:
                return BasicGround(self.screen, SEGMENT_WIDTH)

            case GroundType.PERLIN:
                seed = random.randint(0, 2**32)
                perlinAmplitude = 30
                perlinFrequency = 0.1
                octaves = 2
                interpolation = InterpolationType.COSINE
                return PerlinNoise(
                    seed, 
                    perlinAmplitude, 
                    perlinFrequency, 
                    octaves, 
                    interpolation)
      
    def render(self):
        pass
        
    def run(self):
        self.ground.generate_floor_segment(0)
        active = True
        while active:
            clock = pg.time.Clock()
            clock.tick(60)
            # Sjekker om brukeren har lukket vinduet
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    active = False
            # Farger bakgrunnen lyseblå
            screen.fill((135, 206, 235))
            
            self.ground.update(self.offset)  
            self.ground.render(self.offset)
            self.starting_xx += 1
            self.vision.update(
                Point(self.starting_xx, 300), 
                self.ground
                )              
            match self.ground_type:
                case GroundType.BASIC_GROUND:
                    self.offset += 1
                    
                case GroundType.PERLIN:
                    self.offset += self.offset_speed
                    
            pg.display.flip()
        pg.quit()
        
    def draw_mark(surface, color, coord):
        pg.draw.circle(surface, color, coord, 3)


class Vision:
    eye_position: Point
    sight_width = 10
    x_offset = 10
    near_periphery: Point 
    far_periphery: Point
    
    def __init__(self, eye_position: Point):
        self.near_periphery = None
        self.far_periphery = None
        
    def update(self, eye_position: Point, ground: Ground) -> None:
        """
        Update the vision based on the 
        eye position and the environment.

        Args:
            eye_position (Point): _description_
            environment (Environment): _description_
        """
        self.eye_position = eye_position
        
        x1 = eye_position.x + self.x_offset
        x2 = x1 + self.sight_width
        
        self.near_periphery = Point(x1, ground.get_y(x1))
        self.far_periphery = Point(x2, ground.get_y(x2))
        self.render_vision(screen)

    def render_vision(self, screen):
        pg.draw.circle(
            screen,
            BLACK,
            (self.eye_position.x, self.eye_position.y),
            5,
            2
            )
        pg.draw.line(
            screen, RED, (self.eye_position.x, self.eye_position.y), 
            (self.near_periphery.x, self.near_periphery.y),
            2
            )
        pg.draw.line(
            screen, RED, (self.eye_position.x, self.eye_position.y),
            (self.far_periphery.x, self.far_periphery.y),
            2
            )

    def get_lower_periphery(self):
        return self.near_periphery
    
    def get_upper_periphery(self):
        return self.far_periphery
    
    def get_eye_position(self):
        return self.eye_position

    def get_sight_width(self):
        return self.sight_width
        

if __name__ == "__main__":    
    environment = Environment(screen)
    # Start the main loop
    environment.run()
