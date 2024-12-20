import pymunk
import pygame
from src.agent_parts.limb import Limb
from src.agent_parts.motorjoint import MotorJoint
from src.agent_parts.vision import Vision
from src.ground import Ground
from src.agent_parts.rectangle import Point


class Creature:
    limbs: list[Limb]
    motors: list[MotorJoint]
    vision: Vision

    def __init__(self, space, vision: Vision):
        """
        Initialize a creature with an empty list of limbs and motors.

        """

        self.space = space
        self.limbs = []
        self.motors = []
        self.relative_vectors = []
        self.vision = vision

    def add_limb(
        self,
        width: float,
        height: float,
        position: tuple[float, float],
        mass=1,
        color=(0, 255, 0),
    ) -> Limb:
        """
        Add a limb to the creature.
        Args:
        - width: The width of the limb.
        - height: The height of the limb.
        - position: The position of the limb.
        - mass: The mass of the limb
        - color: The color of the limb.

        """
        limb = Limb(self.space, width, height, position, mass, color)
        self.limbs.append(limb)
        return limb

    def update_vision(self, x: int, y: int):
        """
        Update the vision position of the creature
        Args:
            x (int): x coordinate
            y (int): y coordinate
        """
        self.vision.update(x, y)

    def start_dragging(self, dragged_limb: Limb):
        for limb in self.limbs:
            if limb != dragged_limb:
                vector = (
                    limb.body.position.x - dragged_limb.body.position.x,
                    limb.body.position.y - dragged_limb.body.position.y,
                )
                self.relative_vectors.append((limb, vector))

    def update_creature_position(
        self, dragged_limb: Limb, new_position: tuple[float, float]
    ):
        dragged_limb.body.position = new_position[0], new_position[1]
        for limb, vector in self.relative_vectors:
            new_position = (
                dragged_limb.body.position.x + vector[0],
                dragged_limb.body.position.y + vector[1],
            )
            limb.body.position = new_position

    def add_motor_on_limbs(
        self, limb_a: Limb, limb_b: Limb, position: tuple[float, float]
    ) -> MotorJoint | None:
        if limb_a.contains_point(position) and limb_b.contains_point(position):
            anchor1 = limb_a.global_to_local(position)
            anchor2 = limb_b.global_to_local(position)
            return self.add_motor(limb_a, limb_b, anchor1, anchor2, rate = -10)
        else: 
            return None

    def local_to_global(
        self, limb: Limb, anchor: tuple[float, float]
    ) -> tuple[float, float]:
        """Convert a local anchor point to a global anchor point."""
        return limb.body.local_to_world(anchor)

    def add_motor(
        self,
        limb_a: Limb,
        limb_b: Limb,
        anchor_a: tuple[float, float],
        anchor_b: tuple[float, float],
        rate=0.0,
        tolerance=10,
    ) -> MotorJoint | None:
        """Add a motor connecting two limbs."""
        global_a = self.local_to_global(limb_a, anchor_a)
        global_b = self.local_to_global(limb_b, anchor_b)

        # Check if the global points are within the tolerance
        if (
            abs(global_a[0] - global_b[0]) < tolerance
            and abs(global_a[1] - global_b[1]) < tolerance
        ):
            motor = MotorJoint(
                self.space, limb_a.body, limb_b.body, anchor_a, anchor_b, rate
            )
            self.motors.append(motor)
            return motor

    def local_to_global(
        self, limb: Limb, point: tuple[float, float]
    ) -> tuple[float, float] | None:
        return limb.local_to_global(point)

    def global_to_local(
        self, limb: Limb, point: tuple[float, float]
    ) -> tuple[float, float] | None:
        return limb.global_to_local(point)

    def render(self, screen: pygame.display):
        """Render the entire creature by rendering all limbs."""
        for limb in self.limbs:
            limb.render(screen)
        for motor in self.motors:
            motor.render(screen, motor.pivot.a, motor.pivot.b)  # Render motor joints
        self.vision.render_vision(screen)

    def get_joint_rates(self) -> list[float]:
        """Return the current rates of all motor joints."""
        return [motor.motor.rate for motor in self.motors]

    def get_joint_rotations(self) -> list[float]:
        """Return the current rotations of all motor joints."""
        rotations = []
        for motor in self.motors:
            rotations.append(motor.get_angle())
        return rotations

    def get_amount_of_joints(self) -> int:
        """Return the number of motor joints in the creature."""
        return len(self.motors)

    def get_amount_of_limb(self) -> int:
        """Return the number of limbs in the creature."""
        return len(self.limbs)

    def set_joint_rates(self, rates: list[float]):
        """Set the rates of all motor joints."""
        for motor, rate in zip(self.motors, rates):
            motor.set_motor_rate(rate)

    def get_joint_positions(self) -> list[tuple[float, float]]:
        return [(motor.pivot.a, motor.pivot.b) for motor in self.motors]

    def get_limb_positions(self) -> list[tuple[float, float]]:
        return [(limb.body.position.x, limb.body.position.y) for limb in self.limbs]
