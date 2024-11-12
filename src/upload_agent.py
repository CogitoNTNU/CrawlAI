from src.genome import Genome
from src.agent_parts.creature import Creature

class UploadAgent:
    def __init__(self, genome: Genome, creature: Creature) -> None:
        self.genome = genome
        self.creature = creature
        self.creature_data = creature.to_dict()  # Serialized creature data

    def to_dict(self):
        return {
            'genome': self.genome.to_dict(),
            'creature': self.creature.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        genome = Genome.from_dict(data['genome'])
        creature = Creature.from_dict(data['creature'])
        
        return cls(genome, creature)