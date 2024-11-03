

from typing import List
from src.genome import Genome 
import random
from src.genome import Genome

class GeneticAlgorithm:
      
    speciation = {}  
    species_representatives = {}  

    @staticmethod
    def initialize_population(pop_size: int, num_inputs: int, num_outputs: int) -> List[Genome]:
        """Initialize a population of genomes."""
        population = []
        for genome_id in range(pop_size):
            genome = Genome(genome_id, num_inputs, num_outputs)
            population.append(genome)

            # Initialize the speciation with a key for the genome
            species_id = GeneticAlgorithm.determine_species(genome)

            if species_id not in GeneticAlgorithm.speciation:
                GeneticAlgorithm.speciation[species_id] = []

            GeneticAlgorithm.speciation[species_id].append(genome)

        return population

    @staticmethod
    def determine_species(genome: Genome, speciation_threshold: float = 3.0) -> int:
        """Determine the species ID for a given genome."""
        for species_id, representative in GeneticAlgorithm.species_representatives.items():
            distance = GeneticAlgorithm.delta_function(genome, representative)
            if distance < speciation_threshold:
                return species_id

        # If no existing species matches, create a new species
        new_species_id = len(GeneticAlgorithm.speciation) + 1
        GeneticAlgorithm.species_representatives[new_species_id] = genome
        return new_species_id

    @staticmethod
    def delta_function(genome1: Genome, genome2: Genome, c1=1.0, c2=1.0, c3=0.4) -> float:
        """Calculate the genetic distance (delta) between two genomes."""
        conn1 = {c.innovation_number: c for c in genome1.connections}
        conn2 = {c.innovation_number: c for c in genome2.connections}
        all_innovations = set(conn1.keys()).union(set(conn2.keys()))

        excess_genes = 0
        disjoint_genes = 0
        matching_genes = 0
        weight_difference_sum = 0

        N = max(len(conn1), len(conn2))
        if N < 20:
            N = 1  # Avoid excessive normalization for small genomes

        max_innovation1 = max(conn1.keys(), default=0)
        max_innovation2 = max(conn2.keys(), default=0)

        for innovation_number in all_innovations:
            if innovation_number in conn1 and innovation_number in conn2:
                matching_genes += 1
                weight_difference_sum += abs(conn1[innovation_number].weight - conn2[innovation_number].weight)
            elif innovation_number in conn1 or innovation_number in conn2:
                if innovation_number > max(max_innovation1, max_innovation2):
                    excess_genes += 1
                else:
                    disjoint_genes += 1

        average_weight_difference = (weight_difference_sum / matching_genes) if matching_genes > 0 else 0
        delta = (c1 * excess_genes / N) + (c2 * disjoint_genes / N) + (c3 * average_weight_difference)
        return delta





    def calc_fitness(self, genome: Genome) -> float:
        """
        Calculates the fitness of a given genome. Fitness is defined as the 
        proportion of correct genes in the genome (assumed to be 1).

        Parameters:
        - genome (genome): The genome whose fitness is to be calculated.
        
        Returns:
        - float: The fitness value, between 0 and 1.
        """
    def eval_population(self, population: List[Genome]) -> float:
        """
        Evaluates the entire population's fitness.

        Parameters:
        - population (List[Genome]): A list of genome objects representing 
        the population.
        
        Returns:
        - float: The average fitness of the population.
        """
        



