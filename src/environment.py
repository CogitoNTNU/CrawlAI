import pygame as pg
import random

import itertools
from enum import Enum

from src.ground import Ground, BasicGround, InterpolationType, PerlinNoise
from src.render_object import RenderObject
from src.agent_parts.rectangle import Point
from src.globals import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FONT_SIZE,
    SEGMENT_WIDTH,
    BLACK,
    RED
    )




class GroundType(Enum):
    BASIC_GROUND = 1
    PERLIN = 2


class Environment(RenderObject):
    def __init__(self,  screen, space):
        self.screen = screen
        self.space = space
        self.ground_type = GroundType.BASIC_GROUND
        self.ground: Ground = self.ground_factory(self.ground_type)
        self.starting_xx = 50
        self.point = Point(self.starting_xx, 100)
        self.vision: Vision = Vision(self.point)

        self.offset = 0
        self.offset_speed = 1

    def ground_factory(self, ground_type: GroundType) -> Ground:

        match ground_type:
            case GroundType.BASIC_GROUND:
                return BasicGround(self.screen, self.space, SEGMENT_WIDTH)

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
    
    def update(self):
        self.offset = 1
        self.ground.update(self.offset)
        # self.ground.move_segments(self.offset/100)
        self.starting_xx += 1

    def render(self):
        self.ground.render()

    def run(self):

        if self.ground_type == GroundType.BASIC_GROUND:
            self.ground.generate_floor_segment(0)

        active = True
        while active:
            clock = pg.time.Clock()
            clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    active = False
                    
            self.screen.fill((135, 206, 235))

            self.ground.update(self.offset)
            self.ground.render(self.offset)
            self.starting_xx += 1
            
            match self.ground_type:
                case GroundType.BASIC_GROUND:
                    self.vision.update(
                        self.screen,
                        Point(self.starting_xx, 100),
                        self.ground,
                        self.offset)

                case GroundType.PERLIN:
                    self.vision.update(
                        self.screen,
                        Point(self.starting_xx, 100),
                        self.ground,
                        0)
            self.offset += 1
            pg.display.flip()
        pg.quit()

    def draw_mark(surface, color, coord):
        pg.draw.circle(surface, color, coord, 3)


class Vision:
    eye_position: Point
    sight_width = 50
    x_offset = 50
    near_periphery: Point
    far_periphery: Point

    def __init__(self, eye_position: Point):
        self.eye_position = eye_position
        self.near_periphery = Point(0, 0)
        self.far_periphery = Point(0, 0)

    def update(
            self,
            screen: pg.display,
            eye_position: Point,
            ground: Ground,
            scroll_offset: int
            ) -> None:
        
        self.eye_position = eye_position
        x1 = eye_position.x + self.x_offset
        x2 = x1 + self.sight_width
        try:
            y1=ground.get_y(x1+scroll_offset)
            self.near_periphery = Point(x1, y1)
        except:
            pass
        try:
            y2=ground.get_y(x2+scroll_offset)
            self.far_periphery = Point(x2, y2)
        except:
            pass
     
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
    
    def get_near_periphery(self) -> Point:
        if self.near_periphery is None:
            return Point(0, 0)
        return self.near_periphery
    
    def get_far_periphery(self) -> Point:
        if self.far_periphery is None:
            return Point(0, 0)
        return self.far_periphery



