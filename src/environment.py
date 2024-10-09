from typing import Protocol
import pygame as pg
import random
import math
import time 
import itertools
from enum import Enum



# from src.agent_parts.rectangle import Point

from ground import Ground, BasicGround, InterpolationType, PerlinNoise
from renderObject import RenderObject
from agent_parts.rectangle import Point
# from src.graphics_facade import GraphicsFacade
# from src.agent import Agent

BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255,255,255)

pg.init()


FONT_SIZE = 14
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
FLOOR_HEIGHT = 100
font = pg.font.Font(pg.font.get_default_font(), FONT_SIZE)
Instance=1
perlinSegments = 40


interp_iter = itertools.cycle((InterpolationType.LINEAR, InterpolationType.CUBIC, InterpolationType.COSINE))
show_marks = False


# Create the screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Constants for Ground terrain generation
AMPLITUDE = 40 # Max height of hills
FREQUENCY = 0.05 # Max frequency of hills
SEGMENT_WIDTH = 200  # Width of each terrain segment



class GroundType(Enum):
    BASIC_GROUND = 1
    PERLIN = 2

    

    

class Environment(RenderObject):
    def __init__(self,  screen):
        self.screen = screen
        self.ground: Ground = self.ground_factory(GroundType.PERLIN)
        # TODO: change all references to noise to ground
        
        self.scroll_offset = 0
        self.offset=0
        self.offset_speed=1
        
        
    def ground_factory(self, ground_type: GroundType) -> Ground:
        
        match ground_type:
            case GroundType.BASIC_GROUND:
                return BasicGround(self.screen, SEGMENT_WIDTH)
            case GroundType.PERLIN:
                seed = random.randint(0, 2**32)
                perlinAmplitude = 50
                perlinFrequency = 0.2
                octaves = 2
                perlinSegments = 40
                interpolation = InterpolationType.COSINE
                return PerlinNoise(seed, perlinAmplitude, perlinFrequency, octaves, interpolation)
      
        
 

        
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

            
            if Instance==0:
            # Move the terrain to the left to simulate movement
                self.groundUpdate()
            else:
                self.perlinUpdate()
            # Oppdaterer alt innholdet i vinduet
            # TODO: change all references to noise or groundupdate to ground
            pg.display.flip()

        # Avslutter pg
        pg.quit()

    
    # TDOO: put into basic ground class
    def groundUpdate(self):
        pass
        self.ground.generate_new_floor_segment(self.scroll_offset)
        self.ground.remove_old_floor_segment(self.scroll_offset)
        self.scroll_offset +=1
        self.ground.render(self.scroll_offset)

    def draw_mark(surface, color, coord):
        pg.draw.circle(surface, color, coord, 3)

        
    def perlinUpdate(self):
        # interp_inform = '(I) Interpolation: ' + get_interp_name(self.noise.interp)
        # text_surface = font.render(interp_inform, True, BLACK)
        # screen.blit(text_surface, dest=(SCREEN_WIDTH - text_surface.get_width() - 5, 0))
        # seed_inform = '(S) Seed: ' + str(seed)
        # text_surface = font.render(seed_inform, True, BLACK)
        # screen.blit(text_surface, dest=(SCREEN_WIDTH - text_surface.get_width() - 5, SCREEN_HEIGHT - FONT_SIZE))
        points = list()
        norma = SCREEN_WIDTH / perlinSegments
        for pix_x in range(SCREEN_WIDTH):
            # convert pixel position to real value
            x = (pix_x + self.offset) / norma
            # get perlin noise
            y = self.ground.calculate_y(x)
            # convert perlin noise to pixel height value
            pix_y = SCREEN_HEIGHT / 2 + y
            # check is x value integer in Perlin noise coordinates
            frequency=0.002
            real_x = x * frequency
            if show_marks and math.isclose(real_x, int(real_x), rel_tol=0.001):
                self.draw_mark(screen, RED, (pix_x, pix_y))
            points.append((pix_x, pix_y))
        # draw lines and update display
        pg.draw.lines(screen, (34,139,34), False, points,4)
        pg.display.flip()
        # move Perlin noise
        self.offset += self.offset_speed
    random.seed(time.time())


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
        """_summary_ Update the vision based on the eye position and the environment.

        Args:
            eye_position (Point): _description_
            environment (Environment): _description_
        """
        self.eye_position = eye_position
        
        x1 = eye_position.x + self.x_offset
        x2 = x1 + self.sight_width
        
        self.near_periphery = Point(x1, ground.get_y(x1))
        self.far_periphery = Point(x2, ground.get_y(x2))
        
        
    def get_lower_periphery(self):
        return self.near_periphery
    def get_upper_periphery(self):
        return self.far_periphery
    def get_eye_position(self):
        return self.eye_position

    def get_sight_width(self):
        return self.sight_width
        
        
    


if __name__ == "__main__":
   # Initialize the floor and environment
    
    environment = Environment(screen)
    
    # Start the main loop
    environment.run()
