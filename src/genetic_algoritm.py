

from typing import List
from src.genome import Genome, create_initial_genome
import random
from src.genome import Genome

class GeneticAlgorithm:
    """
    A class that implements a simple genetic algorithm to
    evolve solutions for a problem.
    Manages the population of potential solutions (genomes),
    applies genetic operators
    like selection, crossover, and mutation, and evolves
    the population over generations.
    """
    population_size: int
    mutation_rate: float
    crossover_rate: float    


    speciation = {}


    def __init__(self,
                 population_size: int,
                 mutation_rate: float,
                 crossover_rate: float,
                 elitism_count: int):
        """
        Initializes a new instance of the GeneticAlgorithm class.

        Parameters:
        - population_size (int): The number of genomes in the population.
        - mutation_rate (float): The probability that a gene will be mutated
          in a genome.
        - crossover_rate (float): The probability that a gene will be taken
          from the first parent during crossover.
        - elitism_count (int): The number of top-performing genomes that are
          directly carried over to the next generation.
        """
        
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        

    
    def initialize_population(pop_size: int, num_inputs: int, num_outputs: int) -> List[Genome]:
        """Initialize a population of genomes."""
        population = []
        for genome_id in range(pop_size):
            genome = create_initial_genome(genome_id, num_inputs, num_outputs)
            population.append(genome)
        return population


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
        
    def select_parent(self, population: List[Genome]) -> Genome:
        """
        Selects a parent genome for crossover using a simple tournament
        selection method.

        Parameters:
        - population (List[Genome]): A list of genome objects from which a
        parent will be selected.
        
        Returns:
        - genome: The selected parent genome.
        """
        
    def crossover(self, parent1: Genome, parent2: Genome) -> Genome:
        """
        Performs crossover between two parent genomes to produce a child 
        genome.

        Parameters:
        - parent1 (genome): The first parent genome.
        - parent2 (genome): The second parent genome.
        
        Returns:
        - genome: The child genome resulting from the crossover.
        """
        
    def mutate(genome: Genome, innovation_tracker):
    
    
        
    def evolve(self, population: List[Genome]) -> List[Genome]:
        """
        Evolves the population by performing selection, crossover, 
        and mutation. The top-performing genomes are preserved
        """




