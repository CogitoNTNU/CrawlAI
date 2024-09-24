from typing import Protocol
from CrawlAI.src.genome import Genome
from environment import Environment
from renderObject import RenderObject
from enum import Enum
from agent_parts.limb import Limb, LimbType, limb_factory
from agent_parts.creature import Creature, creature_factory
from agent_parts.rectangle import Rectangle, rectangle_factory
import numpy





GRAVITY = 9.81



class Agent():
    genome: Genome
    creature: Creature
    
    def __init__(self, genome: Genome, creature: Creature):
        self.genome = genome
        self.creature = creature
        
    def get_inputs_from_env(self, env) -> list:
        vision = env.get_vision()
        # TODO: Implement the rest of the inputs, they are the joint angles, health and the position of the limbs.
        pass
    
    def do_inference(self, inputs: list) -> list:
        """_summary_ Do inference on the inputs and return the output.

        Args:
            inputs (list): _description_

        Returns:
            list: outputs
        """
        pass
    
    
    
    
    def act(self, env) -> None:
        self.creature.act(self.do_inference(self.get_inputs_from_env(env)))
        pass

    def save(self, path) -> None:
        pass

    def load(self, path) -> None:
        pass

    def get_genome(self) :
        pass


if __name__ =="__main__":
    import pygame


    rect = rectangle_factory(100, 100, 50, 50)
    limb = limb_factory(rect, 3, 2)

    aurelius = creature_factory(None, [limb], [])
    
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
        window.fill((0, 0, 0))
        pygame.draw.rect(window, (255, 0, 0), (0, 0, 800, 600))
        aurelius.render(window)
        aurelius.updatePosition(0, -GRAVITY)
        pygame.display.flip()
        pygame.time.delay(10)
        
        
    
    pygame.quit()

    
    