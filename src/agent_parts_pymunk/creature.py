import pymunk
import pygame
from limb import Limb
from motorjoint import MotorJoint 

class Creature:
    def __init__(self, space):
        """Initialize a creature with an empty list of limbs and motors."""
        self.space = space
        self.limbs = []
        self.motors = []

    def add_limb(self, width, height, position, mass=1, color=(0, 255, 0)):
        """Add a limb to the creature."""
        limb = Limb(self.space, width, height, position, mass, color)
        self.limbs.append(limb)
        return limb

    def add_motor(self, limb_a, limb_b, anchor_a, anchor_b, rate):
        """Add a motor connecting two limbs."""
        motor = MotorJoint(self.space, limb_a.body, limb_b.body, anchor_a, anchor_b, rate)
        self.motors.append(motor)
        return motor

    def render(self, screen):
        """Render the entire creature by rendering all limbs."""
        for limb in self.limbs:
            limb.render(screen)
        for motor in self.motors:
            motor.render(screen, motor.pivot.a, motor.pivot.b)    # Render motor joints
    
    def get_joint_rates(self):
        """Return the current rates of all motor joints."""
        return [motor.motor.rate for motor in self.motors]

    def set_joint_rates(self, rates):
        """Set the rates of all motor joints."""
        for motor, rate in zip(self.motors, rates):
            motor.set_motor_rate(rate)