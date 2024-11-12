import pymunk
import pygame
import math


class MotorJoint:
    def __init__(self, space, limb_a, limb_b, anchor_a, anchor_b, rate):
        """Initialize a motor joint between two limbs."""
        body_a = limb_a.body
        body_b = limb_b.body
        self.pivot = pymunk.PivotJoint(body_a, body_b, anchor_a, anchor_b)
        self.motor = pymunk.SimpleMotor(body_a, body_b, rate)
        self.anchor_a = anchor_a
        self.anchor_b = anchor_b
        self.limb_a = limb_a
        self.limb_b = limb_b
        
        space.add(self.pivot, self.motor)

    def set_motor_rate(self, rate):
        """Set the rotation speed of the motor."""
        self.motor.rate = rate

    def render(self, screen, body_a, body_b):
        """Render the motor joint as a small red circle between the two bodies."""
        # Get the positions of the two bodies
        pos_a_world = body_a.local_to_world(self.pivot.anchor_a)
        # Draw a red circle connecting the two bodies
        pygame.draw.circle(
            surface=screen,
            color=(255, 0, 0),
            center=(float(pos_a_world.x), float(pos_a_world.y)),
            radius=3,
        )

    def get_angle(self):
        """Get the angle of the motor joint."""
        return self.pivot.angle
