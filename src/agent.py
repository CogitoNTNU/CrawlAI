from abc import ABC, abstractmethod
import pybox2d
from enum import Enum
import tensorflow as tf

from src.enviroment import Enviroment
from src.renderObject import RenderObject
from src.genome import Genome
from src.agent_parts.creature import Creature
class LimbType(Enum):  """ Summary: Enum for the different types of limbs.
    """
    FOOT = 1
    LEG = 2
    LIMB = 3


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



    
    