import pygame as pg
import random
import math

from renderObject import RenderObject
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
AMPLITUDE = 50  # Height of hills
FREQUENCY = 0.02  # Frequency of hills
SEGMENT_WIDTH = 100  # Width of each terrain segment



class Environment(RenderObject):
    def __init__(self,  screen):
        self.screen = screen
        self.ground = Ground(screen, AMPLITUDE, FREQUENCY, SEGMENT_WIDTH)
        self.scroll_offset = 0
        
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
        self.scroll_offset +=5
        self.ground.render(self.scroll_offset)


        

       

    
class Ground(RenderObject):
    def __init__(self, screen, amplitude, frequency, segment_width):
        self.screen = screen
        self.amplitude = amplitude
        self.frequency = frequency
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
        floor= []
        for x in range(start_x, start_x + self.segment_width + 1, 10):
            y = int(SCREEN_HEIGHT - FLOOR_HEIGHT + self.amplitude * math.sin(self.frequency * x))
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












if __name__ == "__main__":
   # Initialize the floor and environment
    
    environment = Environment(screen)
    
    # Start the main loop
    environment.run()

       
        



            
            
