import pymunk
import pygame
from src.agent_parts.limb import Limb
from src.agent_parts.motorjoint import MotorJoint  


class Creature:

    def __init__(self, space):
        """Initialize a creature with an empty list of limbs and motors."""
        self.space = space
        self.limbs = []
        self.motors = []

    def add_limb(self, width: float, height: float, position: tuple[float,float], mass=1, color=(0, 255, 0)) -> Limb:
        """Add a limb to the creature."""
        limb = Limb(self.space, width, height, position, mass, color)
        self.limbs.append(limb)
        return limb

    def add_motor(self, limb_a: Limb, limb_b: Limb, anchor_a: tuple[float,float], anchor_b: tuple[float,float], rate: float, tolerance: float) -> MotorJoint|None:
        """Add a motor connecting two limbs."""
        if(abs(limb_a.body.position + anchor_a - limb_b.body.position + anchor_b) < tolerance):
            motor = MotorJoint(self.space, limb_a.body, limb_b.body, anchor_a, anchor_b, rate)
            self.motors.append(motor)
            return motor

    def render(self, screen: pygame.display):
        """Render the entire creature by rendering all limbs."""
        for limb in self.limbs:
            limb.render(screen)
        for motor in self.motors:
            motor.render(screen, motor.pivot.a, motor.pivot.b)    # Render motor joints
    
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

    def set_joint_rates(self, rates: float): 
        """Set the rates of all motor joints."""
        for motor, rate in zip(self.motors, rates):
            motor.set_motor_rate(rate)
    
    def get_joint_positions(self) -> list[tuple[float,float]]:
        return [(motor.pivot.a, motor.pivot.b) for motor in self.motors]
    
    