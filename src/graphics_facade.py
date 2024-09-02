

from pygame import *
from typing import Protocol


# Pygame documentation:
# https://www.pygame.org/docs/

# How to use protocols:
# https://andrewbrookins.com/technology/building-implicit-interfaces-in-python-with-protocol-classes/

class Graphics(Protocol):
    def draw(self, image, x, y) -> None:
        pass

    def clear(self) -> None:
        pass

    def update(self) -> None:
        pass

    def get_screen(self) -> Surface:
        pass

    def get_background(self) -> Surface:
        pass
    

class GraphicsFacade():
    def __init__(self):
        self.screen = display.set_mode((800, 600))
        self.background = Surface((800, 600))
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        display.flip()

    def draw(self, image, x, y):
        self.screen.blit(image, (x, y))

    def clear(self):
        self.screen.blit(self.background, (0, 0))

    def update(self):
        display.flip()

    def get_screen(self):
        return self.screen

    def get_background(self):
        return self.background
    
