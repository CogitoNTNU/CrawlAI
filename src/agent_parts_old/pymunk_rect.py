import numpy as np
import pygame
import math
import pymunk  # Importing Pymunk

from CrawlAI.src.agent_parts.rectangle import Point


class Rectangle:
    def __init__(self,
                 point: Point,
                 width: float,
                 height: float,
                 mass: float = 1.0
                 ):
        """
        Initializes a Rectangle object and its corresponding
        Pymunk physics body.
        
        Parameters:
        ----------
        point : Point
            The initial position of the rectangle.
        width : float
            The width of the rectangle.
        height : float
            The height of the rectangle.
        mass : float, optional
            The mass of the rectangle for physics simulation.
        """
        x, y = point.x, point.y
        self.width = width
        self.height = height

        self.poPoints = np.array([ 
            np.array([x, y]),
            np.array([x + width, y]),
            np.array([x + width, y + height]),
            np.array([x, y + height])
        ])

        # Calculate moment of inertia for a rectangle
        moment = pymunk.moment_for_box(mass, (width, height))

        # Create a dynamic Pymunk body
        self.body = pymunk.Body(mass, moment)
        self.body.position = x + width / 2, y + height / 2

        # Define the polygon shape
        vertices = [
            (-width / 2, -height / 2),
            (width / 2, -height / 2),
            (width / 2, height / 2),
            (-width / 2, height / 2),
        ]
        self.shape = pymunk.Poly(self.body, vertices)
        self.shape.friction = 0.7  

    def update_from_physics(self):
        """
        Updates the rectangle's corner points based on the Pymunk 
        body's position and rotation.
        """
        cx, cy = self.body.position  # Center of the rectangle
        angle = self.body.angle  # Rotation angle of the rectangle

        # Calculate the rotated points around the center
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        half_width = self.width / 2
        half_height = self.height / 2

        # New corner positions
        self.poPoints[0] = np.array([
            cx - half_width * cos_angle + half_height * sin_angle,
            cy - half_width * sin_angle - half_height * cos_angle
        ])
        self.poPoints[1] = np.array([
            cx + half_width * cos_angle + half_height * sin_angle,
            cy + half_width * sin_angle - half_height * cos_angle
        ])
        self.poPoints[2] = np.array([
            cx + half_width * cos_angle - half_height * sin_angle,
            cy + half_width * sin_angle + half_height * cos_angle
        ])
        self.poPoints[3] = np.array([
            cx - half_width * cos_angle - half_height * sin_angle,
            cy - half_width * sin_angle + half_height * cos_angle
        ])

    def apply_force(self, force, offset=(0, 0)):
        """
        Applies a force to the Pymunk body.

        Parameters:
        ----------
        force : tuple
            The force to apply as (fx, fy).
        offset : tuple
            The point at which to apply the force, 
            relative to the center of the body.
        """
        self.body.apply_force_at_local_point(force, offset)

    def apply_impulse(self, impulse, offset=(0, 0)):
        """
        Applies an impulse to the Pymunk body.

        Parameters:
        ----------
        impulse : tuple
            The impulse to apply as (ix, iy).
        offset : tuple
            The point at which to apply the impulse, 
            relative to the center of the body.
        """
        self.body.apply_impulse_at_local_point(impulse, offset)

    def render(self, window):
        """
        Renders the rectangle on a given window using pygame.

        Parameters:
        ----------
        window : any
            The graphical window where the rectangle will be drawn.
        """
        pygame.draw.polygon(
            window,
            (255, 255, 255),
            [(p[0], p[1]) for p in self.poPoints]
            )

    def updatePosition(self, point: Point):
        """
        Updates the position of the rectangle (manually)
        by translating its corner points.
        This method is not used in physics mode,
        where the position is updated via Pymunk.
        """
        x, y = point.x, point.y
        translation = np.array([x, y])
        self.poPoints += translation


def rectangle_factory(
            point: Point,
            width: float,
            height: float,
            mass: float = 1.0):
    """
    Factory function for creating a Rectangle object with physics.

    Parameters:
    ----------
    point : Point
        The initial position of the rectangle.
    width : float
        The width of the rectangle.
    height : float
        The height of the rectangle.
    mass : float
        The mass of the rectangle for physics simulation.

    Returns:
    -------
    Rectangle:
        A new instance of the Rectangle class.
    """
    return Rectangle(point, width, height, mass)
