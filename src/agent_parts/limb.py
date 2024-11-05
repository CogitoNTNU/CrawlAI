import pymunk
import pygame


class Limb:
    def __init__(self, space, width, height, position, mass=1, color=(0, 255, 0)):
        """Initialize a limb as a rectangular body."""
        self.width = width
        self.height = height
        self.color = color

        # Create a dynamic body with mass
        self.body = pymunk.Body(mass, pymunk.moment_for_box(mass, (width, height)))
        self.body.position = position
        
        # Create a box shape for the limb
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        
        self.shape.friction = 1
        self.shape.filter = pymunk.ShapeFilter(categories=0b1, mask=pymunk.ShapeFilter.ALL_MASKS() ^ 0b1)
   
        space.add(self.body, self.shape)

    def render(self, screen):
        """
        Render the limb onto the screen.
        Args:
        - screen: The pygame surface to render onto.
        """
        # Get the position and angle from the pymunk body
        pos = self.body.position
        angle = self.body.angle
        # Calculate the vertices of the rectangle in world coordinates
        vertices = self.shape.get_vertices()
        vertices = [v.rotated(angle) + pos for v in vertices]
        # Convert pymunk Vec2d vertices to pygame coordinates
        vertices = [(float(v.x), float(v.y)) for v in vertices]
        # Draw the polygon onto the screen
        pygame.draw.polygon(surface=screen, color=(0, 255, 0), points=vertices, width=0)