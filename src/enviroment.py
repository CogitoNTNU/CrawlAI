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



class Enviroment(RenderObject):
    def __init__(self, state, terrain_segments, ):
        self.state = state
        self.terrain_segments = terrain_segments
        
    # Generate a segment of the floor
    def generate_starting_floor(start_x: float) -> list:
        """Generates a segment of the floor
        Args: start_x (float): The x-coordinate of the starting point of the segment
        Returns: list: A list of points representing the floor segment
        """
        floor_points = []
        for x in range(start_x, start_x + SEGMENT_WIDTH + 1, 10):
            y = int(SCREEN_HEIGHT - FLOOR_HEIGHT + AMPLITUDE * math.sin(FREQUENCY * x))
            floor_points.append((x, y))
        return floor_points

    def generate_new_floor_segment(self, start_x, terrain_segments):
    # Generate new segments if needed
        if terrain_segments[-1][-1][0] - scroll_offset < SCREEN_WIDTH:
            # Generate a new segment at the rightmost part of the terrain
            last_x = terrain_segments[-1][-1][0]
            terrain_segments.append(generate_floor_segment(last_x))

    def reset(self):
        screen.fill((135, 206, 250))  # Sky blue background

    def render(self,terrain_segments, scroll_offset):
        for segment in terrain_segments:
            shifted_points = [(x - scroll_offset, y) for (x, y) in segment]
            # Add points to close the polygon and fill the bottom of the screen
            shifted_points.append((shifted_points[-1][0], SCREEN_HEIGHT))
            shifted_points.append((shifted_points[0][0], SCREEN_HEIGHT))
            pg.draw.polygon(screen, (34, 139, 34), shifted_points)  # Green hills

class Ground(RenderObject):
    def __init__(self, screen):
        self.screen = screen
        self.color = (0, 0, 0)
        self.ground = pg.Rect(0, 400, 800, 200)

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.ground)

    def update(self):
        pass
    
    def render(self):
        self.draw()


# active = True
# while active:
#     clock = pg.time.Clock()
#     clock.tick(60)
#     # Sjekker om brukeren har lukket vinduet
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             active = False
#     # Farger bakgrunnen lyseblå
#     screen.fill((135, 206, 235))

#     # Oppdaterer alt innholdet i vinduet
#     pg.display.flip()

# # Avslutter pg
# pg.quit()









if __name__ == "__main__":
    # main()
    # Screen dimensions


# Generate a segment of the floor
    def generate_floor_segment(start_x):
        floor_points = []
        for x in range(start_x, start_x + SEGMENT_WIDTH + 1, 10):
            y = int(SCREEN_HEIGHT - FLOOR_HEIGHT + AMPLITUDE * math.sin(FREQUENCY * x))
            floor_points.append((x, y))
        return floor_points

# Main game loop
    def main():
        clock = pg.time.Clock()
        
        # Starting terrain
        terrain_segments = [generate_floor_segment(0)]
        scroll_offset = 0  # How much we've moved to the right

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            # Clear the screen
            screen.fill((135, 206, 250))  # Sky blue background

            # Move the terrain to the left to simulate movement
            scroll_offset += 5  # Speed of movement to the right

            # Generate new segments if needed
            if terrain_segments[-1][-1][0] - scroll_offset < SCREEN_WIDTH:
                # Generate a new segment at the rightmost part of the terrain
                last_x = terrain_segments[-1][-1][0]
                terrain_segments.append(generate_floor_segment(last_x))

            # Remove old segments that are off-screen
            if terrain_segments[0][-1][0] - scroll_offset < -SEGMENT_WIDTH:
                terrain_segments.pop(0)

            # Draw the terrain
            for segment in terrain_segments:
                shifted_points = [(x - scroll_offset, y) for (x, y) in segment]
                # Add points to close the polygon and fill the bottom of the screen
                shifted_points.append((shifted_points[-1][0], SCREEN_HEIGHT))
                shifted_points.append((shifted_points[0][0], SCREEN_HEIGHT))
                pg.draw.polygon(screen, (34, 139, 34), shifted_points)  # Green hills

            # Flip the display
            pg.display.flip()

            # Cap the frame rate
            clock.tick(60)

        pg.quit()

