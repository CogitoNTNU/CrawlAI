from typing import Protocol

class Agent(Protocol):
    def act(self, env) -> int:
        pass

    def save(self, path) -> None:
        pass

    def load(self, path) -> None:
        pass

    def get_genome(self) :
        pass

class Creature():
    def __init__(self, env):
        self.env = env

def creature_factory(env):
    return Creature(env)

class Limb():
    length: float
    
    def __init__(self):
        pass


class Joint():
    angle: float
    limb1: Limb
    limb2: Limb
    
    def __init__(self):
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

    
    