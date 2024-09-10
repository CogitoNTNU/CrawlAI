from typing import Protocol
from enviroment import Enviroment
from renderObject import RenderObject


class Agent(Protocol):
    def act(self, env) -> int:
        pass

    def save(self, path) -> None:
        pass

    def load(self, path) -> None:
        pass

    def get_genome(self) :
        pass



if __name__ =="__main__":
    import pygame

    aurelius = creature_factory(None)
    
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        pygame.display.flip()
        pygame.time.delay(10)

    
    