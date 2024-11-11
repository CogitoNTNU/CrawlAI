import random
from typing import List, Tuple

from src.genome import Genome, Innovation
from src.species import Species


class GeneticAlgorithm:
    def __init__(self, population_size: int, num_inputs: int, num_outputs: int):
        self.population_size = population_size
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.population: List[Genome] = []
        self.species_list: List[Species] = []
        self.innovation = Innovation.get_instance()
        self.genome_id_counter = 0
        self.species_id_counter = 0

        self.initialize_population()

    def initialize_population(self):
        for _ in range(self.population_size):
            genome = Genome(
                genome_id=self.genome_id_counter,
                num_inputs=self.num_inputs,
                num_outputs=self.num_outputs,
            )
            self.population.append(genome)
            self.genome_id_counter += 1

    def evaluate_fitness(self, evaluate_function):
        for genome in self.population:
            genome.fitness = evaluate_function(genome)

    def speciate(self, compatibility_threshold: float):
        self.species_list = []
        for genome in self.population:
            found_species = False
            for species in self.species_list:
                representative = species.members[0]
                distance = genome.compute_compatibility_distance(representative)
                if distance < compatibility_threshold:
                    species.add_member(genome)
                    genome.species = species.species_id
                    found_species = True
                    break
            if not found_species:
                new_species = Species(self.species_id_counter)
                new_species.add_member(genome)
                genome.species = new_species.species_id
                self.species_list.append(new_species)
                self.species_id_counter += 1

    def adjust_fitness(self):
        for species in self.species_list:
            species.adjust_fitness()

    def reproduce(self):
        new_population = []
        total_average_fitness = sum(
            species.average_fitness for species in self.species_list
        )
        for species in self.species_list:
            offspring_count = int(
                (species.average_fitness / total_average_fitness) * self.population_size
            )
            for _ in range(offspring_count):
                parent1 = species.select_parent()
                if random.random() < 0.25:
                    # Mutation without crossover
                    child = parent1.copy()
                    child.mutate()
                else:
                    parent2 = species.select_parent()
                    child = parent1.crossover(parent2)
                    child.mutate()
                child.genome_id = self.genome_id_counter
                self.genome_id_counter += 1
                new_population.append(child)
        # If we don't have enough offspring due to rounding, fill up the population
        while len(new_population) < self.population_size:
            parent = random.choice(self.population)
            child = parent.copy()
            child.mutate()
            child.genome_id = self.genome_id_counter
            self.genome_id_counter += 1
            new_population.append(child)
        self.population = new_population

    def evolve(
        self, generations: int, evaluate_function, compatibility_threshold: float
    ):
        for generation in range(generations):
            print(f"Generation {generation+1}")
            self.evaluate_fitness(evaluate_function)
            self.speciate(compatibility_threshold)
            self.adjust_fitness()
            self.reproduce()
