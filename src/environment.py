import pygame as pg
import random
import math
import time 
from abc import ABC, abstractmethod

from src.agent_parts.rectangle import Point
from src.renderObject import RenderObject
# from src.graphics_facade import GraphicsFacade
# from src.agent import Agent

BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pg.init()



SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
FLOOR_HEIGHT = 100

# Create the screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Constants for terrain generation
AMPLITUDE_MIN = 30  # Minimum height of hills
AMPLITUDE_MAX = 40 # Max height of hills
FREQUENCY_MIN = 0.01  # Minimum frequency of hills
FREQUENCY_MAX = 0.05 # Max frequency of hills
SEGMENT_WIDTH = 700  # Width of each terrain segment

    


class Environment(RenderObject):
    def __init__(self,  screen):
        self.screen = screen
        self.ground = Ground(screen, SEGMENT_WIDTH)
        self.scroll_offset = 0
        
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

            
            
            # Move the terrain to the left to simulate movement

            self.update()
            # Oppdaterer alt innholdet i vinduet
            pg.display.flip()

        # Avslutter pg
        pg.quit()


    def update(self):
        self.ground.generate_new_floor_segment(self.scroll_offset)
        self.ground.remove_old_floor_segment(self.scroll_offset)
        self.scroll_offset +=1
        self.ground.render(self.scroll_offset)



    
        
        



class AbstractGround(ABC):
    @abstractmethod
    def generate_floor_segment(self, start_x: float) -> list:
        pass

    @abstractmethod
    def generate_new_floor_segment(self, scroll_offset: int):
        pass

    @abstractmethod
    def remove_old_floor_segment(self, scroll_offset: float):
        pass

    



class PerlinGround(RenderObject, AbstractGround):

    defeault_amplitude = 30








    
class Ground(RenderObject, AbstractGround):
    def __init__(self, screen, segment_width):
        self.screen = screen
       
        self.segment_width = segment_width
        self.terrain_segments = []

        self.terrain_segments.append(self.generate_floor_segment(0))


    def generate_floor_segment(self, start_x : float) -> list:
        """
        Generates a segment of the floor
        
        Args:
            start_x (float): The x-coordinate of the starting point of the segment
        returns:
            list: A list of points representing the floor segment 
        """
        amplitude = random.randint(AMPLITUDE_MIN, AMPLITUDE_MAX)
        frequency = random.uniform(FREQUENCY_MIN, FREQUENCY_MAX)

        floor= []
        for x in range(start_x, start_x + self.segment_width + 1, 1):
            y = int(SCREEN_HEIGHT - FLOOR_HEIGHT + AMPLITUDE_MAX * math.sin(frequency * x))
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
    alpha = 0.5
    sight_widht = 0.5
    beta = alpha + sight_widht
    lower_periphery: Point 
    upper_periphery: Point
    angle_speed = 0.1
    
    def __init__(self, eye_position: Point):
        self.lower_periphery = None
        self.upper_periphery = None
        
    def move_eye(self) -> None:
        """_summary_ Move the eye by increasing the alpha and beta angles by the angle_speed.
        """
        self.alpha += self.angle_speed
        self.beta += self.angle_speed
        
        
    def update(self, eye_position: Point, ground: Ground) -> None:
        """_summary_ Update the vision based on the eye position and the environment.

        Args:
            eye_position (Point): _description_
            environment (Environment): _description_
        """
        self.eye_position = eye_position
        self.move_eye()
        
        # LA STÅ!!!!
        # self.lower_periphery.x = intersection mellom linje og bakken                      
        # self.upper_periphery = intersection mellom linje og bakken
        
    
    def get_alpha(self):
        return self.alpha
    def get_beta(self):
        return self.beta
    def get_lower_periphery(self):
        return self.lower_periphery
    def get_upper_periphery(self):
        return self.upper_periphery
    def get_eye_position(self):
        return self.eye_position
    def get_angle_speed(self):
        return self.angle_speed
    def get_sight_width(self):
        return self.sight_widht
        
        
    








if __name__ == "__main__":
   # Initialize the floor and environment
    
    environment = Environment(screen)
    
    # Start the main loop
    environment.run()

       
        



            
            

