from abc import ABC, abstractmethod
import pybox2d
from enum import Enum
import tensorflow as tf

from src.genome import Genome
from src.environment import Environment
from src.render_object import RenderObject

from src.agent_parts_old.limb import Limb, LimbType, limb_factory
from src.agent_parts_old.creature import Creature, creature_factory


class Agent(ABC):
    """
    
    """
    genome: Genome
    creature: Creature
    
    def __init__(self, genome: Genome, creature: Creature) -> None:
        self.genome = genome
        self.creature = creature

    @abstractmethod
    def act(self, env) -> int:
        pass

    def save(self, path: str) -> None:
        """
        Saves the agent and it's creature to a file.
        """
        pass

    def load(self, path: str) -> None:
        """
        Loads the agent and it's creature from a file."""
        pass

    def get_genome(self) -> Genome:
        """
        Returns the genome of the agent.
        """
        return self.genome
    
    @abstractmethod
    def get_enviroment_state(self, env) -> tf.Tensor:
        """
        Creates the input tensor based on the agent's enviroment and body.
        """
        pass

