from typing import Protocol
import pygame as pg
import random
import math
from enum import Enum
import pymunk

from render_object import RenderObject
from globals import (SCREEN_WIDTH,
                     SCREEN_HEIGHT,
                     PERLIN_SEGMENTS,
                     RED,
                     SEGMENT_WIDTH,
                     FLOOR_HEIGHT,
                     AMPLITUDE,
                     FREQUENCY
                     )

pg.init()

show_marks = False

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class InterpolationType(Enum):
    LINEAR = 1
    COSINE = 2
    CUBIC = 3


class Ground(Protocol):
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
    def swap_floor_segments(self, scroll_offset: float):
        pass

    @property
    def get_y(self, x: int) -> int:
        pass

    @property
    def render(self, scroll_offset: float):
        # TODO: removew this later, when we call render from another 
        # place than environment
        pass

    @property
    def calculate_y(self, x: int) -> int:
        # TODO: remove this later
        pass

    @property
    def update(self):
        pass


class BasicSegment():
    def __init__(self, start_x: int, end_x: int) -> None:
        self.start_x = start_x
        self.end_x = end_x
        self.points = []

    def add_points(self, start_x: int, end_x: int) -> None:
        for x in range(start_x, end_x + 1, 1):
            y = int(
                SCREEN_HEIGHT - FLOOR_HEIGHT + AMPLITUDE * math.sin(
                    FREQUENCY * x)
                )
            self.points.append((x, y))

    def get_points(self) -> list:
        return self.points
    
    def init_pymunk_polygon(self, space) -> None:
        self.body = pymunk.Body(0, 0, 1)
        self.poly = pymunk.Poly(self.body, self.points, radius=0.0)
        space.add(self.body, self.poly)

    def remove_pymunk_polygon(self,space) -> None:
        space.remove(self.body, self.poly)



class BasicGround(RenderObject, Ground, BasicSegment):
    def __init__(self, screen: pg.display, segment_width: int) -> None:
        self.screen = screen
   
        self.segment_width = segment_width
        self.terrain_segments: BasicSegment = []

        self.terrain_segments.append(
            self.generate_floor_segment(0))
        self.terrain_segments.append(
            self.generate_floor_segment(self.segment_width))
        
    def get_current_segment(self, x: int) -> int:
        """
        Get the index of the segment that
        contains the x-coordinate

        Args:
            x (int): _description_ The x-coordinate

        Returns:
            int: _description_ The index of the segment that contains the 
            x-coordinate
        """
        return x // SEGMENT_WIDTH
        
    def get_y(self, x: int) -> int:
        """_summary_ Get the y-coordinate of the terrain at the x-coordinate

        Args:
            x (int): _description_ The x-coordinate

        Returns:
            int: _description_ The y-coordinate of the terrain at the 
            x-coordinate
        """
        start_segment = self.terrain_segments[0]
        starting_x: int = start_segment.get_points()[0][0]//SEGMENT_WIDTH
        correct_index = self.get_current_segment(x) - starting_x
        points = self.terrain_segments[correct_index]
        
        for point in points.get_points():
            if point[0] == x:
                return point[1]
            
        raise ValueError("The x-coordinate is not in the terrain segment")
        
    def update(self, scroll_offset: float) -> None:
        self.generate_new_floor_segment(scroll_offset)
        self.remove_old_floor_segment(scroll_offset)
        # self.swap_floor_segments(scroll_offset)
        scroll_offset += 1

    def generate_floor_segment(self, start_x: int) -> list:
        """
        Generates a segment of the floor
        
        Args:
            start_x (float): The x-coordinate of the starting point 
            of the segment
        returns:
            list: A list of points representing the floor segment
        """

        segment = BasicSegment(start_x, start_x + SEGMENT_WIDTH)
        segment.add_points(start_x, start_x + SEGMENT_WIDTH)
        return segment

    def generate_new_floor_segment(self, scroll_offset: int) -> None:
        """_summary_ Generate a new floor segment

        Args:
            scroll_offset (int): _description_
        """
        last_segment = self.terrain_segments[-1]
        if last_segment.get_points()[-1][0] - scroll_offset < SCREEN_WIDTH:
            # Generate a new segment at the rightmost part of the terrain
            last_x = last_segment.get_points()[-1][0]
            self.terrain_segments.append(self.generate_floor_segment(last_x))

    def remove_old_floor_segment(self, scroll_offset: float) -> None:
        # Remove old segments that are off-
        last_segment = self.terrain_segments[-1]
        if last_segment.get_points()[-1][0] - scroll_offset < -SEGMENT_WIDTH:
            self.terrain_segments.pop(0)
    
    def swap_floor_segments(self, scroll_offset: float) -> None:
        """_summary_ Swap the floor segments"""
        
        if (self.terrain_segments[0][-1][0] - self.scroll_offset 
                < -SEGMENT_WIDTH):
            # Move the first segment to the right end of the second segment
            last_segment_end_x = self.terrain_segments[1][-1][0]
            new_start_x = last_segment_end_x + 1
            self.terrain_segments[0] = self.generate_floor_segment(new_start_x)
            # Swap the segments in the list so they alternate
            self.terrain_segments.append(self.terrain_segments.pop(0))

    def render(self, scroll_offset: float) -> None:  
        """Render screen objects

        Args:
            terrain_segments (_type_): _description_
            scroll_offset (_type_): _description_
        """
        for segment in self.terrain_segments:
            shifted_points = [(x - scroll_offset, y) for (x, y) in segment.get_points()]
            # Add points to close the polygon and fill the bottom of the screen
            shifted_points.append((shifted_points[-1][0], SCREEN_HEIGHT))
            shifted_points.append((shifted_points[0][0], SCREEN_HEIGHT))
            pg.draw.polygon(screen, (34, 139, 34), shifted_points)
            

class PerlinSegment():
    def __init__(self, start_x: int, end_x: int) -> None:
        self.start_x = start_x
        self.end_x = end_x
        self.points = []

    def add_points(self, start_x: int, end_x: int) -> None:
       pass

    def get_points(self) -> list:
        return self.points
    
    def init_pymunk_polygon(self, space) -> None:
        body = pymunk.Body(0, 0, 1)
        poly = pymunk.Poly(body, self.points, radius=0.0)
        space.add(body, poly)


class PerlinNoise():

    def __init__(
                self,
                seed,
                amplitude=1,
                frequency=0.002,
                octaves=1,
                interp=InterpolationType.COSINE,
                use_fade=False
                ) -> None:
        
        self.seed = random.Random(seed).random()
        self.amplitude = amplitude
        self.frequency = frequency
        self.octaves = octaves
        self.interp = interp
        self.use_fade = use_fade
        self.coordinates = list()
        self.render_points = list()
        self.norma = SCREEN_WIDTH / PERLIN_SEGMENTS
        self.floor_segments = list()
        
        self.mem_x = dict()
    
    def generate_floor_segment(self, offset: int) -> None:
        """_summary_ Generate a segment of the floor

        Args:
            offset (int): _description_
        """
        pass
                
    def update(self, offset: int) -> None:
        """Update the screen objects

        Args:
            offset (int): The current offset for the scrolling terrain
        """
        self.offset = offset  # Store the offset for use in other methods
        points = list()
        norma = SCREEN_WIDTH / PERLIN_SEGMENTS
        for pix_x in range(SCREEN_WIDTH+SEGMENT_WIDTH):
            x = (pix_x + offset) / norma
            y = self.generate_y(x)
            pix_y = SCREEN_HEIGHT / 2 + y
            if show_marks and math.isclose(
                    x * self.frequency,
                    int(x * self.frequency),
                    rel_tol=0.001
                    ):
                self.draw_mark(screen, RED, (pix_x, pix_y))
            points.append((pix_x, pix_y))
        self.render_points = points

    def render(self, offset) -> None:
        """_summary_ Render the screen objects
        args: offset is just for matching the function signature
        """
        # draw lines and update display
        pg.draw.lines(
            screen, 
            (34, 139, 34),
            False,
            self.render_points,
            4
            )
        pg.display.flip()

    def __noise(self, x) -> float:
        """
        _summary_ Generate a random number for the given x

        Args:
            x (_type_): _description_

        Returns:
            _type_: _description_
        """
        # made for improve performance
        if x not in self.mem_x:
            self.mem_x[x] = random.Random(self.seed + x).uniform(-1, 1)
        return self.mem_x[x]

    def draw_mark(surface: pg.Surface, color, coord: tuple) -> None:
        """
        _summary_ Draw a mark on the screen

        Args:
            surface (pg.Surface): _description_
            color (_type_): _description_
            coord (tuple): _description_
        """
        pg.draw.circle(surface, color, coord, 3)

    def __interpolated_noise(self, x: int) -> float:
        """
        _summary_ Interpolate the noise at the given x

        Args:
            x (_type_): _description_

        Returns:
            float: result of interpolation
        """
        prev_x = int(x)  # previous integer
        next_x = prev_x + 1  # next integer
        frac_x = x - prev_x  # fractional of x

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

    def get_y(self, x: int) -> int:
        """_summary_ Get the y-coordinate of the terrain at the x-coordinate

        Args:
            x (int): _description_ The x-coordinate

        Returns:
            int: _description_ The y-coordinate of the terrain at the 
            x-coordinate
        """
    
        norma = SCREEN_WIDTH / PERLIN_SEGMENTS
        real_x = (x + self.offset) / norma
        y = self.generate_y(real_x)
        pix_y = SCREEN_HEIGHT / 2 + y
        return pix_y

    def generate_y(self, x: int) -> int:
        """_summary_ Calculate the y value of the Perlin noise at the given x

        Args:
            x (int):

        Returns:
            float: y
        """
        frequency = self.frequency
        amplitude = self.amplitude
        result = 0
        for _ in range(self.octaves):
            result += self.__interpolated_noise(x * frequency) * amplitude
            frequency *= 2
            amplitude /= 2

        return result

    def __cosine_interp(self, a, b, x) -> float:
        x2 = (1 - math.cos(x * math.pi)) / 2
        return a * (1 - x2) + b * x2
