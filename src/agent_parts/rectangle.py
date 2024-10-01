import numpy as np 
import pygame
import math 

class Point:
    """
    A class representing a 2D point in space.

    Attributes:
    ----------
    x : float
        The x-coordinate of the point.
    y : float
        The y-coordinate of the point.
    """

    def __init__(self, x: float, y: float):
        """
        Initializes a Point object.

        Parameters:
        ----------
        x : float
            The x-coordinate of the point.
        y : float
            The y-coordinate of the point.
        """
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """
        Returns a string representation of the Point object.

        Returns:
        -------
        str:
            The string format of the point's coordinates as "X: {x}, Y: {y}".
        """
        return f"X: {self.x}, Y: {self.y}"


class Rectangle:
    """
    A class representing a 2D rectangle using its position, width, and height.

    Attributes:
    ----------
    width : float
        The width of the rectangle.
    height : float
        The height of the rectangle.
    poPoints : np.ndarray
        A np array representing the four corner points of the rectangle.
    """

    def __init__(self, x: float, y: float, width: float, height: float):
        """
        Initializes a Rectangle object.

        Parameters:
        ----------
        x : float
            The x-coordinate of the rectangle's top-left corner.
        y : float
            The y-coordinate of the rectangle's top-left corner.
        width : float
            The width of the rectangle.
        height : float
            The height of the rectangle.

        The rectangle is represented by four points using np arrays.
        """
        self.width = width
        self.height = height
        self.poPoints = np.array([   
                                        np.array([x, y]),
                                        np.array([x + height, y]),
                                        np.array([x + height, y + width]),
                                        np.array([x, y + width])
                                    ])

    def contains(self, point: Point) -> bool:
        """
        Checks if a given point is inside the rectangle using linear algebra.

        Parameters:
        ----------
        point : Point
            The point to be checked.

        Returns:
        -------
        bool:
            True if the point is inside the rectangle, False otherwise.
        """
        for i in range(4):
            x1 = self.poPoints[i][0]
            y1 = self.poPoints[i][1]
            x2 = self.poPoints[(i + 1) % 4][0]
            y2 = self.poPoints[(i + 1) % 4][1]
            xp = point.x
            yp = point.y
            # Cross product
            crossProduct = (yp - y1) * (x2 - x1) - (xp - x1) * (y2 - y1)
            if crossProduct < 0:
                return False
        return True

    def intersects(self, other_rect) -> bool:
        """
        Checks if this rectangle intersects with another rectangle.

        Parameters:
        ----------
        other_rect : Rectangle
            The rectangle to check for intersection with.

        Returns:
        -------
        bool:
            True if the rectangles intersect, False otherwise.
        """
        return not (other_rect.x > self.poPoints[0][0] + self.width or 
                    other_rect.x + other_rect.width < self.poPoints[0][0] or 
                    other_rect.y > self.poPoints[0][1] + self.height or 
                    other_rect.y + other_rect.height < self.poPoints[0][1])

    def __str__(self) -> str:
        """
        Returns a string representation of the Rectangle object.

        Returns:
        -------
        str:
            The string format of the rectangle's position and size as "X: {x}, Y: {y}, Width: {width}, Height: {height}".
        """
        return f"X: {self.poPoints[0][0]}, Y: {self.poPoints[0][1]}, Width: {self.width}, Height: {self.height}"

    def render(self, window):
        """
        Renders the rectangle on a given window using pygame.

        Parameters:
        ----------
        window : any
            The graphical window where the rectangle will be drawn.
        """
        pygame.draw.polygon(window, (255, 255, 255), ((self.poPoints[0][0], self.poPoints[0][1]), 
                                                      (self.poPoints[1][0], self.poPoints[1][1]), 
                                                      (self.poPoints[2][0], self.poPoints[2][1]), 
                                                      (self.poPoints[3][0], self.poPoints[3][1])))

    def updatePosition(self, x: float, y: float):
        """
        Updates the position of the rectangle by translating its corner points.

        Parameters:
        ----------
        x : float
            The amount to translate the rectangle in the x direction.
        y : float
            The amount to translate the rectangle in the y direction.
        """
        translation = np.array([x, y])
        self.poPoints = self.poPoints + translation

    def rotateRectangle(self, angle: float):
        widthVector = np.array([self.width * math.cos(angle), self.width * math.sin(angle)])
        heightVector = np.array([-self.height *math.sin(angle), self.height * math.cos(angle)])
        x0, y0 = self.x , self.y
        x1, y1 = x0 + widthVector[0] , y0 + widthVector[1]
        x2, y2 = x0 + heightVector[0] , y0 + heightVector[1]
        x3, y3 = x0 + widthVector[0] + heightVector[0], y0 + widthVector[1] + heightVector[1]

        return x0, y0, x1, y1, x2, y2, x3, y3


def rectangle_factory(x: float, y: float, width: float, height: float) -> Rectangle:
    """
    Factory function for creating a Rectangle object.

    Parameters:
    ----------
    x : float
        The x-coordinate of the rectangle's top-left corner.
    y : float
        The y-coordinate of the rectangle's top-left corner.
    width : float
        The width of the rectangle.
    height : float
        The height of the rectangle.

    Returns:
    -------
    Rectangle:
        A new instance of the Rectangle class.
    """
    return Rectangle(x, y, width, height)
