import pygame as pg
from src.agent_parts.rectangle import Point
from src.ground import Ground
from src.globals import BLACK, RED


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

    def update(self, eye_position: Point, ground: Ground, scroll_offset: int) -> None:

        self.eye_position = eye_position
        x1 = eye_position.x + self.x_offset
        x2 = x1 + self.sight_width
        try:
            y1 = ground.get_y(x1 + scroll_offset)
            self.near_periphery = Point(x1, y1)
        except:
            pass
        try:
            y2 = ground.get_y(x2 + scroll_offset)
            self.far_periphery = Point(x2, y2)
        except:
            pass

    def render_vision(self, screen):
        pg.draw.circle(screen, BLACK, (self.eye_position.x, self.eye_position.y), 5, 2)
        pg.draw.line(
            screen,
            RED,
            (self.eye_position.x, self.eye_position.y),
            (self.near_periphery.x, self.near_periphery.y),
            2,
        )
        pg.draw.line(
            screen,
            RED,
            (self.eye_position.x, self.eye_position.y),
            (self.far_periphery.x, self.far_periphery.y),
            2,
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
