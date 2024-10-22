from enum import Enum
import numpy as np

from src.render_object import RenderObject
from src.agent_parts.rectangle import Rectangle, Point
import math


class LimbType(Enum):
    """
    Enum representing the different types of limbs a creature can have.
    
    Attributes:
    ----------
    LIMB : int
        Represents a standard limb (value 1).
    HEAD : int
        Represents the head of the creature (value 2).
    FOOT : int
        Represents the foot of the creature (value 3).
    """
    LIMB = 1
    HEAD = 2     
    FOOT = 3


class Limb(RenderObject):
    """
    A class representing a limb of a creature, 
    which is a subclass of RenderObject.

    Attributes:
    ----------
    rect : Rectangle
        A Rectangle object representing the shape and position of the limb.
    damage_scale : float
        The scale of damage this limb can take, determined by its type.
    orientation : float
        The orientation or angle of the limb in the environment.
    limbType : LimbType
        An instance of LimbType indicating the specific type of limb 
        (LIMB, HEAD, or FOOT).
    """

    rect: Rectangle
    damage_scale: float
    jointList: list[RenderObject]

    def __init__(self,
                 rect: Rectangle,
                 damage_scale: float,
                 limbType: LimbType
                 ):
        """
        Initializes a Limb object.

        Parameters:
        ----------
        rect : Rectangle
            The rectangle representing the shape and size of the limb.
        damage_scale : float
            A value representing how much damage the limb can take.
        limbType : LimbType
            The type of the limb (LIMB, HEAD, or FOOT).
        """
        self.rect = rect
        self.damage_scale = damage_scale
        self.limbType = limbType
        self.jointList = []

    def rotate(self, angle: float):
        """
        Rotates the limb by a given angle.

        Parameters:
        ----------
        angle : float
            The angle by which to rotate the limb, 
            added to the current orientation.
        """
        self.rect.rotateRectangle(angle)
        for joint in self.jointList:
            self.updateRenderObject(joint)
    
    def inherit_orientation(self, 
                            parent_orientation: float,
                            limb_orientation: float):
        """
        Inherits the orientation from the parent and adds 
        the limb's own orientation.

        Parameters:
        ----------
        parent_orientation : float
            The orientation of the parent limb or object.
        limb_orientation : float
            The local orientation of the limb, relative to the parent.
        """
        # self.orientation = parent_orientation + limb_orientation
        pass
    
    def updateRenderObject(self, renderObject: RenderObject):
        
        renderObject_relative_pos = renderObject.get_relative_position()
        rect_pos = self.rect.get_position()
        rect_angle = self.rect.get_angle()

        final_x, final_y = self.rect.rotatePointPoint(
            rect_angle,
            renderObject_relative_pos,
            Point(rect_pos.x+1, rect_pos.y))

        renderObject.set_position(Point(final_x, final_y))
    
    def updatePosition(self, x: float, y: float):
        """
        Updates the position of the limb by updating the 
        position of its rectangle.

        Parameters:
        ----------
        x : float
            The new x-coordinate of the limb.
        y : float
            The new y-coordinate of the limb.
        """
        self.rect.updatePosition(x, y)

    def render(self, window):
        """
        Renders the limb on the provided window.

        Parameters:
        ----------
        window : any
            The graphical window or surface where the limb will be rendered.
        """
        self.rect.render(window)
        for joint in self.jointList:
            joint.render(window)

    def addJoint(self, joint: RenderObject): 
        if (self.rect.contains(joint.get_position())):
            self.jointList.append(joint)

            joint_pos = joint.get_position()
            rect_pos = self.rect.get_position()
            rectangle_angle = self.rect.get_angle()

            angle, _ = self.rect.angle_between_vectors(
                np.array([math.cos(rectangle_angle),
                          math.sin(rectangle_angle)
                          ]),
                np.array([joint_pos.x-rect_pos.x, joint_pos.y-rect_pos.y]))
            relative_x, relative_y = self.rect.rotatePointPoint(
                angle,
                joint_pos,
                rect_pos
                )
            joint.set_relative_position(Point(relative_x, relative_y))


def limb_factory(
        rect: Rectangle,
        limbType: LimbType,
        orientation: float
        ) -> Limb:
    """
    Factory function for creating a Limb object.

    Parameters:
    ----------
    rect : Rectangle
        A Rectangle object representing the limb's shape and position.
    limbType : LimbType
        The type of limb to be created (LIMB, HEAD, or FOOT).
    orientation : float
        The initial orientation angle of the limb.

    Returns:
    -------
    Limb:
        A new instance of the Limb class with the appropriate damage 
        scale based on the limb type.
    """
    damage_scale: float = 0
    match limbType:
        case 1:
            damage_scale = 0.1  # Low damage scale for a standard limb
        case 2:
            damage_scale = 1.0  # High damage scale for the head
        case 3:
            damage_scale = 0.0  # No damage for the foot
        case _:
            return "Invalid LimbType"
    return Limb(rect, damage_scale, limbType)
