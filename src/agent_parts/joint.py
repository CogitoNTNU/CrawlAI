from CrawlAI.src.render_object import RenderObject
import pygame as pg
from src.agent_parts.limb import Limb
from src.agent_parts.rectangle import Point


class Joint(RenderObject):

    """
    The Joint class represents a connection between two limbs, providing a 
    point of articulation or rotation between them. The joint tracks the angle 
    of rotation, and the relative positions of the two limbs connected by it.

    Attributes:
        angle (float): The current angle of the joint, representing the 
                       rotation between the two limbs.
        limb1 (Limb): The first limb connected to the joint.
        limb2 (Limb): The second limb connected to the joint.
        position1 (list[float, float]): The position of the 
        joint on the first limb.
        position2 (list[float, float]): The position of the j
        oint on the second limb.
    """

    angle: float
    limbChild: Limb
    point: Point
    relative_point: Point

    def __init__(self, angle: float, point: Point):
        """
        Initializes a Joint object.

        Args:
            angle (float): The initial angle of the joint.
            limb1 (Limb): The first limb to be connected to the joint.
            limb2 (Limb): The second limb to be connected to the joint.
            position1 (list[float, float]): The position on the first
            limb where the joint is attached.
            position2 (list[float, float]): The position on the second
            limb where the joint is attached.
        """
        self.angle = angle
        self.limbChild = None
        self.point = point
        self.relative_point = None

    def get_position(self):
        return self.point
    
    def set_position(self, point: Point):
        self.point = point
    
    def render(self, window):
        """
        This method is responsible for rendering the joint visually.
        It is currently a placeholder method, and should be implemented in
        subclasses or future revisions if visual representation is required.
        """
        print(self.point.x, self.point.y)
        radius = min(window.get_width(), window.get_height())*0.005
        pg.draw.circle(window, (0, 0, 0), (self.point.x, self.point.y), radius)
        if (self.limbChild is not None):
            self.limbChild.render(window)

    def rotate(self, angle: float):
        """
        Rotates the joint by a given angle, modifying the current joint angle.

        Args:
            angle (float): The angle (in degrees or radians, based on 
            the system) by which the joint should be rotated.
        """
        self.angle += angle
        
    def get_angle(self):
        """
        Returns the current angle of the joint.

        Returns:
            float: The current angle of the joint.
        """
        return self.angle
    
    def set_angle(self, angle: float):
        """
        Sets the angle of the joint to a specific value.

        Args:
            angle (float): The new angle to set for the joint.
        """
        self.angle = angle

    def set_relative_position(self, point: Point):
        self.relative_point = point

    def get_relative_position(self):
        return self.relative_point


def joint_factory(angle: float, point: Point) -> Joint:
    """
    Factory function for creating a Joint object between two limbs.

    This function simplifies the creation of a Joint object between a 
    parent limb and a child limb. It returns a Joint instance, but the 
    specific positions and angles are assumed to be handled inside the 
    factory function (may need modification based on the actual usage).

    Args:
        parent (Limb): The parent limb that will be connected to the joint.
        child (Limb): The child limb that will be connected to the joint.

    Returns:
        Joint: A new Joint instance connecting the parent and child limbs.
    """
    return Joint(angle, point)