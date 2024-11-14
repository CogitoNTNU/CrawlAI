import pymunk
import pygame


class Limb:
    def __init__(self, space, width, height, position, mass=3, color=(0, 255, 0)):
        """Initialize a limb as a rectangular body."""
        self.width = width
        self.height = height
        self.color = color
        self.mass = mass

        # Create a dynamic body with mass
        self.body = pymunk.Body(mass, pymunk.moment_for_box(mass, (width, height)))
        self.body.position = position

        # Create a box shape for the limb
        self.shape = pymunk.Poly.create_box(self.body, (width, height))

        self.shape.friction = 1
        self.shape.filter = pymunk.ShapeFilter(
            categories=0b1, mask=pymunk.ShapeFilter.ALL_MASKS() ^ 0b1
        )

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

    def contains_point(self, point: tuple[float, float]) -> bool:
        """
        Check if a given point is inside the limb.

        Args:
        - point: A tuple representing the x and y coordinates of the point.

        Returns:
        - True if the point is inside the limb, False otherwise.
        """
        x, y = point
        point_vec = pymunk.Vec2d(x, y)

        # Perform a point query to check if the point is within the shape
        return self.shape.point_query(point_vec).distance <= 0

    def global_to_local(
        self, position: tuple[float, float]
    ) -> tuple[float, float] | None:
        if not isinstance(position, (tuple, list)) or len(position) != 2:
            raise ValueError(
                "Position must be a tuple or list with two elements: (x, y)"
            )

        # Convert position to Vec2d
        global_position = pymunk.Vec2d(position[0], position[1])

        # Transform from global to local coordinates
        local_position = self.body.world_to_local(global_position)

        return float(local_position.x), float(local_position.y)

    def local_to_global(
        self, position: tuple[float, float]
    ) -> tuple[float, float] | None:
        if not isinstance(position, (tuple, list)) or len(position) != 2:
            raise ValueError(
                "Position must be a tuple or list with two elements: (x, y)"
            )

        # Convert position to Vec2d
        local_position = pymunk.Vec2d(position[0], position[1])

        # Transform from local to global coordinates
        global_position = self.body.local_to_world(local_position)

        return float(global_position.x), float(global_position.y)

    def to_string(self) -> str:
        return f"Limb: width={self.width}, height={self.height}, mass={self.mass}, position={self.body.position}"
