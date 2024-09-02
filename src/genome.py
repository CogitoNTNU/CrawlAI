





from dataclasses import dataclass

@dataclass
class Genome:
    """Genome class for the AI"""
    id: int
    fitness: float
    nodes: list
    connections: list
    species: int
    adjusted_fitness: float
    network: object

    def __str__(self):
        return f"Genome ID: {self.id}, Fitness: {self.fitness}, Species: {self.species}, Adjusted Fitness: {self.adjusted_fitness}"


    def __repr__(self):
        return f"Genome ID: {self.id}, Fitness: {self.fitness}, Species: {self.species}, Adjusted Fitness: {self.adjusted_fitness}"


    def __eq__(self, other):
        return self.id == other.id


    def __lt__(self, other):
        return self.fitness < other.fitness