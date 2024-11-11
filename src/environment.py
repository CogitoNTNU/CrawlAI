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
    RED,
)


class GroundType(Enum):
    BASIC_GROUND = 1
    PERLIN = 2


class Environment(RenderObject):

    def __init__(self, screen, space):
        self.screen = screen
        self.space = space
        self.ground_type = GroundType.BASIC_GROUND
        self.ground: Ground = self.ground_factory(self.ground_type)
        self.starting_xx = 50
        self.point = Point(self.starting_xx, 100)
        self.offset = 0
        self.offset_speed = 1
        self.death_ray = None

    def activate_death_ray(self):
        self.death_ray = DeathRay(20)

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
                    seed, perlinAmplitude, perlinFrequency, octaves, interpolation
                )

    def update(self):
        self.offset = 0
        self.ground.update(self.offset)
        # self.ground.move_segments(self.offset/100)
        self.starting_xx += 1
        if self.death_ray is not None:
            self.death_ray.move(0.1)

    def render(self):
        self.ground.render()
        if self.death_ray is not None:
            self.death_ray.render(self.screen)

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
                        self.offset,
                    )

                case GroundType.PERLIN:
                    self.vision.update(
                        self.screen, Point(self.starting_xx, 100), self.ground, 0
                    )
            self.offset += 1
            pg.display.flip()
        pg.quit()

    def draw_mark(surface, color, coord):
        pg.draw.circle(surface, color, coord, 3)


class DeathRay:
    x: int

    def __init__(self, x: int):
        self.x = x

    def update(self, x: int):
        self.x = x

    def render(self, screen):
        pg.draw.line(screen, RED, (self.x, 0), (self.x, SCREEN_HEIGHT), 2)

    def move(self, offset: int):
        self.x += offset

    def get_x(self):
        return self.x
