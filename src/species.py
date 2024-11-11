import random
from typing import List
from src.genome import Genome


class Species:
    def __init__(self, species_id: int):
        self.species_id = species_id
        self.members: List[Genome] = []
        self.average_fitness: float = 0.0

    def add_member(self, genome: Genome):
        self.members.append(genome)

    def adjust_fitness(self):
        total_fitness = sum(genome.fitness for genome in self.members)
        for genome in self.members:
            genome.adjusted_fitness = genome.fitness / len(self.members)
        self.average_fitness = total_fitness / len(self.members)
