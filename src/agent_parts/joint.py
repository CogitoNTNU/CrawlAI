from environment import Environment
from renderObject import RenderObject
from agent_parts.limb import Limb

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
        position1 (list[float, float]): The position of the joint on the first limb.
        position2 (list[float, float]): The position of the joint on the second limb.
    """

    angle: float
    limb1: Limb
    limb2: Limb
    position1: list[float, float]
    position2: list[float, float]

    def __init__(self, angle: float, limb1: Limb, limb2: Limb, position1: list[float, float], position2: list[float, float]):
        """
        Initializes a Joint object.

        Args:
            angle (float): The initial angle of the joint.
            limb1 (Limb): The first limb to be connected to the joint.
            limb2 (Limb): The second limb to be connected to the joint.
            position1 (list[float, float]): The position on the first limb where the joint is attached.
            position2 (list[float, float]): The position on the second limb where the joint is attached.
        """
        self.angle = angle
        self.limb1 = limb1
        self.limb2 = limb2
        self.position1 = position1
        self.position2 = position2
    
    def render(self):
        """
        This method is responsible for rendering the joint visually.
        It is currently a placeholder method, and should be implemented in 
        subclasses or future revisions if visual representation is required.
        """
        pass

    def rotate(self, angle: float):
        """
        Rotates the joint by a given angle, modifying the current joint angle.

        Args:
            angle (float): The angle (in degrees or radians, based on the system) 
                           by which the joint should be rotated.
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


def joint_factory(parent: Limb, child: Limb) -> Joint:
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
    return Joint()