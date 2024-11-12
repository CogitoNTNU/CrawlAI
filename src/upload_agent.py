from src.genome import Genome


class UploadAgent:
    def __init__(self, genome: Genome, creature_data: dict):
        self.genome = genome
        self.creature_data = creature_data  # Serialized creature data

    def to_dict(self):
        return {
            'genome': self.genome.to_dict(),
            'creature': self.creature_data,
        }

    @classmethod
    def from_dict(cls, data):
        genome = Genome.from_dict(data['genome'])
        creature_data = data['creature']
        return cls(genome, creature_data)