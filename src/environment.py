from typing import Protocol
import pygame as pg
import random
import math
import time 
import itertools
from enum import Enum


from abc import ABC, abstractmethod

# from src.agent_parts.rectangle import Point
from src.renderObject import RenderObject
from src.agent_parts.rectangle import Point
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
Instance=0
perlinSegments = 40


# Create the screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Constants for Ground terrain generation
AMPLITUDE = 40 # Max height of hills
FREQUENCY = 0.05 # Max frequency of hills
SEGMENT_WIDTH = 200  # Width of each terrain segment


class InterpolationType(Enum):
    LINEAR = 1
    COSINE = 2
    CUBIC = 3


# set initial parametrs Perlinground generation

interp_iter = itertools.cycle((InterpolationType.LINEAR, InterpolationType.CUBIC, InterpolationType.COSINE))
show_marks = False


class GroundType(Enum):
    GROUND = 1
    PERLIN = 2

    

    

class Environment(RenderObject):
    def __init__(self,  screen):
        self.screen = screen
        self.ground: BaseGround = self.ground_factory(GroundType.PERLIN)
        # TODO: change all references to noise to ground
        self.scroll_offset = 0
        self.offset=0
        self.offset_speed=1
        
        
    def ground_factory(self, ground_type: GroundType) -> BaseGround:
        if ground_type == GroundType.GROUND:
            return Ground(self.screen, SEGMENT_WIDTH)
        elif ground_type == GroundType.PERLIN:
            seed = random.randint(0, 2**32)
            perlinAmplitude = 50
            perlinFrequency = 0.2
            octaves = 2
            perlinSegments = 40
            interpolation = InterpolationType.COSINE
            return PerlinNoise(seed, perlinAmplitude, perlinFrequency, octaves, interpolation)
        else:
            raise ValueError("Invalid ground type")

        
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
            pg.display.flip()

        # Avslutter pg
        pg.quit()

    
    def groundUpdate(self):
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
            y = self.noise.get(x)

            # convert perlin noise to pixel height value
            pix_y = SCREEN_HEIGHT / 2 + y

            # check is x value integer in Perlin noise coordinates
            real_x = x * self.noise.frequency
            if show_marks and math.isclose(real_x, int(real_x), rel_tol=0.001):
                self.draw_mark(screen, RED, (pix_x, pix_y))

            points.append((pix_x, pix_y))

        # draw lines and update display
        pg.draw.lines(screen, (34,139,34), False, points,4)
        pg.display.flip()

        # move Perlin noise
        self.offset += self.offset_speed


        
    
    random.seed(time.time())


class BaseGround(Protocol):
    @property
    def generate_floor_segment(self, start_x: float) -> list:
        pass

    @property
    def generate_new_floor_segment(self, scroll_offset: int):
        pass

    @property
    def remove_old_floor_segment(self, scroll_offset: float):
        pass

    @property
    def get_y(self, x: int) -> int:
        pass


class Ground(RenderObject, BaseGround):
    def __init__(self, screen, segment_width):
        self.screen = screen
       
        self.segment_width = segment_width
        self.terrain_segments = []

        self.terrain_segments.append(self.generate_floor_segment(0))
        
    def get_current_segment(x: int) -> int:
        """_summary_ Get the index of the segment that contains the x-coordinate

        Args:
            x (int): _description_ The x-coordinate

        Returns:
            int: _description_ The index of the segment that contains the x-coordinate
        """
        return x // SEGMENT_WIDTH
        
    def get_y(self, x: int) -> int:
        """_summary_ Get the y-coordinate of the terrain at the x-coordinate

        Args:
            x (int): _description_ The x-coordinate

        Returns:
            int: _description_ The y-coordinate of the terrain at the x-coordinate
        """
        points = self.terrain_segments[self.get_current_segment(x)]
        
        for point in points:
            if point[0] == x:
                return point[1]
            
        raise ValueError("The x-coordinate is not in the terrain segment")
        

    
            
    
        
        
            
            
    def generate_floor_segment(self, start_x : float) -> list:
        """
        Generates a segment of the floor
        
        Args:
            start_x (float): The x-coordinate of the starting point of the segment
        returns:
            list: A list of points representing the floor segment 
        """

        floor= []
        for x in range(start_x, start_x + self.segment_width + 1, 1):
            y = int(SCREEN_HEIGHT - FLOOR_HEIGHT + AMPLITUDE * math.sin(FREQUENCY * x))
            floor.append((x, y))
        return floor
    

    def generate_new_floor_segment(self, scroll_offset: int):
    # Generate new segments if needed
        
        if self.terrain_segments[-1][-1][0] - scroll_offset < SCREEN_WIDTH:
            # Generate a new segment at the rightmost part of the terrain
            last_x = self.terrain_segments[-1][-1][0]
            self.terrain_segments.append(self.generate_floor_segment(last_x))

    def remove_old_floor_segment(self, scroll_offset: float):
        # Remove old segments that are off-screen
            if self.terrain_segments[0][-1][0] - scroll_offset < -SEGMENT_WIDTH:
                self.terrain_segments.pop(0)
    
    
    def render(self,scroll_offset: float):    
        
        """Render screen objects

        Args:
            terrain_segments (_type_): _description_
            scroll_offset (_type_): _description_
        """
        

        for segment in self.terrain_segments:
            shifted_points = [(x - scroll_offset, y) for (x, y) in segment]
            # Add points to close the polygon and fill the bottom of the screen
            shifted_points.append((shifted_points[-1][0], SCREEN_HEIGHT))
            shifted_points.append((shifted_points[0][0], SCREEN_HEIGHT))
            pg.draw.polygon(screen, (34, 139, 34), shifted_points)  # Green hills





    

class Vision:
    eye_position: Point
    sight_width = 10
    x_offset = 10
    near_periphery: Point 
    far_periphery: Point
    

    
    def __init__(self, eye_position: Point):
        self.near_periphery = None
        self.far_periphery = None
        
    
    def update(self, eye_position: Point, ground: BaseGround) -> None:
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
        
        
    
    def get_alpha(self):
        return self.alpha
    def get_beta(self):
        return self.beta
    def get_lower_periphery(self):
        return self.near_periphery
    def get_upper_periphery(self):
        return self.far_periphery
    def get_eye_position(self):
        return self.eye_position
    def get_angle_speed(self):
        return self.angle_speed
    def get_sight_width(self):
        return self.sight_width
        
        
    

class PerlinNoise():

   def __init__(self, 
            seed, amplitude=1, frequency=0.002,
            octaves=1, interp=InterpolationType.COSINE, use_fade=False):
        self.seed = random.Random(seed).random()
        self.amplitude = amplitude
        self.frequency = frequency
        self.octaves = octaves
        self.interp = interp
        self.use_fade = use_fade

        self.mem_x = dict()


   def __noise(self, x):
        # made for improve performance
        if x not in self.mem_x:
            self.mem_x[x] = random.Random(self.seed + x).uniform(-1, 1)
        return self.mem_x[x]


   def __interpolated_noise(self, x):
        prev_x = int(x) # previous integer
        next_x = prev_x + 1 # next integer
        frac_x = x - prev_x # fractional of x

        if self.use_fade:
            frac_x = self.__fade(frac_x)

        # intepolate x
        if self.interp is InterpolationType.LINEAR:
            res = self.__linear_interp(
                self.__noise(prev_x), 
                self.__noise(next_x),
                frac_x)
        elif self.interp is InterpolationType.COSINE:
            res = self.__cosine_interp(
                self.__noise(prev_x), 
                self.__noise(next_x),
                frac_x)
        else:
            res = self.__cubic_interp(
                self.__noise(prev_x - 1), 
                self.__noise(prev_x), 
                self.__noise(next_x),
                self.__noise(next_x + 1),
                frac_x)

        return res


   def get(self, x):
        frequency = self.frequency
        amplitude = self.amplitude
        result = 0
        for _ in range(self.octaves):
            result += self.__interpolated_noise(x * frequency) * amplitude
            frequency *= 2
            amplitude /= 2

        return result



   def __cosine_interp(self, a, b, x):
        x2 = (1 - math.cos(x * math.pi)) / 2
        return a * (1 - x2) + b * x2



if __name__ == "__main__":
   # Initialize the floor and environment
    
    environment = Environment(screen)
    
    # Start the main loop
    environment.run()
