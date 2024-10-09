import numpy as np 
import pygame
import math 
from src.renderObject import RenderObject

class Point:
    x: float
    y: float
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

    class anchor: 
        x: float 
        y : float

        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y
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

    def __init__(self, point: Point, width: float, height: float):
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
        x, y = point.x, point.y
        self.width = width
        self.height = height
        self.poPoints = np.array([ 
                                        np.array([x,y]),
                                        np.array([x + width, y]),
                                        np.array([x + width, y + height]), 
                                        np.array([x, y + height])

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

    def updatePosition(self, point: Point):
        """
        Updates the position of the rectangle by translating its corner points.

        Parameters:
        ----------
        x : float
            The amount to translate the rectangle in the x direction.
        y : float
            The amount to translate the rectangle in the y direction.
        """
        x, y = point.x, point.y

        self.poPoints[0][0] += x
        self.poPoints[0][1] += y
        
        self.poPoints[1][0] += x
        self.poPoints[1][1] += y

        self.poPoints[2][0] += x
        self.poPoints[2][1] += y

        self.poPoints[3][0] += x
        self.poPoints[3][1] += y

        """translation = np.array([x, y])
        self.poPoints = self.poPoints + translation"""
    
    def get_angle(self):
        x1,y1= self.poPoints[0][0], self.poPoints[0][1]
        x2,y2= self.poPoints[1][0], self.poPoints[1][1]

        angle, _ = self.angle_between_vectors(np.array([1,0]),np.array([x2-x1,y2-y1]))
        if y2-y1 < 0:
            angle=2*math.pi-angle
        return angle



    def rotateRectangle(self, angle: float):
        """Returns the coordinates of the edges of the rectangle after rotation"""
        widthVector = np.array([self.width * math.cos(angle), self.width * math.sin(angle)])
        heightVector = np.array([-self.height *math.sin(angle), self.height * math.cos(angle)])
        self.poPoints[1][0], self.poPoints[1][1] = self.poPoints[0][0] + widthVector[0] , self.poPoints[0][1] + widthVector[1]
        self.poPoints[2][0], self.poPoints[2][1] = self.poPoints[0][0] + widthVector[0] + heightVector[0], self.poPoints[0][1] + widthVector[1] + heightVector[1]
        self.poPoints[3][0], self.poPoints[3][1] = self.poPoints[0][0] + heightVector[0] , self.poPoints[0][1] + heightVector[1]
    
    
    def rotateAnchor(self, angle:float):
        """Rotates the special point in the rectangle with a given angle"""
        anchorVector = np.array([self.anchor.x - self.x, self.anchor.y - self.y])
        x_rotated = anchorVector[0]*math.cos(angle) - anchorVector[1]*math.sin(angle)
        y_rotated = anchorVector[0]*math.sin(angle) - anchorVector[1]*math.cos(angle)

        self.anchor.x = x_rotated
        self.anchor.y = y_rotated

    def rotateAroundPoint(self, angle: float , point: Point): 
        """Rotates the rectangle around a point with a given coordinate"""
        x, y = point.x, point.y
        for i in range(4):
            pointVector = np.array([self.poPoints[i][0] - x, self.poPoints[i][1] - y])
            x_rotated = pointVector[0]*math.cos(angle) - pointVector[1]*math.sin(angle)
            y_rotated = pointVector[0]*math.sin(angle) - pointVector[1]*math.cos(angle)
            self.poPoints[i][0] = x_rotated
            self.poPoints[i][1] = y_rotated
    
    def rotateRenderObject(self, angle: float, renderObject: RenderObject, axisPoint: Point):
        """Rotates the position of the renderObject around the given axisPoint by the specified angle."""
        objectPoint = renderObject.get_position()
        
        final_x, final_y =self.rotatePointPoint(angle, objectPoint, axisPoint)
        # Set the new position
        renderObject.set_position(Point(final_x, final_y))

    def rotatePointPoint(self, angle: float, objectPoint: Point, axisPoint: Point):
        o_x = objectPoint.x
        o_y = objectPoint.y

        a_x = axisPoint.x
        a_y = axisPoint.y

        # Translate point to origin (relative to axisPoint)
        translated_x = o_x - a_x
        translated_y = o_y - a_y


        
        obj_angle, _ = self.angle_between_vectors(np.array([1,0]),np.array([translated_x,translated_y]))

        if translated_y < 0:
            obj_angle=2*math.pi-obj_angle

        r=math.sqrt(translated_x**2 + translated_y**2)
        # Apply rotation
        # x_rotated = translated_x * math.cos(angle) - translated_y * math.sin(angle)
        # y_rotated = translated_x * math.sin(angle) + translated_y * math.cos(angle)
        print(obj_angle, angle)
        # Translate back to original position
        final_x = a_x+r * math.cos(angle+obj_angle)
        final_y = a_y+r * math.sin(angle+obj_angle)

        return final_x, final_y

    def get_position(self) -> Point:
        x=self.poPoints[0][0]
        y=self.poPoints[0][1]
        return Point(x,y)
    
    def angle_between_vectors(self, A, B):

        # Step 1: Compute the dot product
        dot_product = np.dot(A, B)
        
        # Step 2: Calculate the magnitudes (norms) of the vectors
        magnitude_A = np.linalg.norm(A)
        magnitude_B = np.linalg.norm(B)
        
        # Step 3: Calculate the cosine of the angle
        cos_angle = dot_product / (magnitude_A * magnitude_B)
        
        # Step 4: Use arccos to find the angle in radians
        angle_radians = np.arccos(np.clip(cos_angle, -1.0, 1.0))  # Clip is used to handle floating point errors
        
        # Step 5: Convert radians to degrees (optional)
        angle_degrees = np.degrees(angle_radians)
        
        return angle_radians, angle_degrees

        

def rectangle_factory(point: Point, width: float, height: float) -> Rectangle:
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
    return Rectangle(point, width, height)
