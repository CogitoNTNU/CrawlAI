from typing import Protocol
from enum import Enum
import numpy

from src.genome import Genome
from src.environment import Environment
from src.render_object import RenderObject

from src.agent_parts_old.limb import Limb, LimbType, limb_factory
from src.agent_parts_old.creature import Creature, creature_factory
from CrawlAI.src.agent_parts.rectangle import Rectangle, rectangle_factory


class Agent():
    genome: Genome
    creature: Creature
    
    def __init__(self, genome: Genome, creature: Creature):
        self.genome = genome
        self.creature = creature
        
    def get_inputs_from_env(self, env) -> list:
        vision = env.get_vision()
        # TODO: Implement the rest of the inputs, they are the joint angles, 
        # health and the position of the limbs.
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

    def get_genome(self) -> Genome:
        pass
