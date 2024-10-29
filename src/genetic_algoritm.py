

from typing import List
from src.genome import Genome
import random


class GeneticAlgorithm:
    """
    A class that implements a simple genetic algorithm to evolve solutions for a problem.
    Manages the population of potential solutions (genomes), applies genetic operators 
    like selection, crossover, and mutation, and evolves the population over generations.
    """
    population_size: int
    mutation_rate: float
    crossover_rate: float    

    def __init__(self, population_size: int, mutation_rate: float, crossover_rate: float, elitism_count: int):
        """
        Initializes a new instance of the GeneticAlgorithm class.

        Parameters:
        - population_size (int): The number of genomes in the population.
        - mutation_rate (float): The probability that a gene will be mutated in a genome.
        - crossover_rate (float): The probability that a gene will be taken from the first parent during crossover.
        - elitism_count (int): The number of top-performing genomes that are directly carried over to the next generation.
        """
        
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        
    def init_population(self, genome_length: int) -> List[Genome]:
        """
        Initializes the population with random genomes.

        Parameters:
        - genome_length (int): The length of each genome.
        
        Returns:
        - List[genome]: A list of genome objects representing the initial population.
        """

        self.genome_length = genome_length

    def calc_fitness(self, genome: Genome) -> float:
        """
        Calculates the fitness of a given genome. Fitness is defined as the proportion of correct genes in the genome (assumed to be 1).

        Parameters:
        - genome (genome): The genome whose fitness is to be calculated.
        
        Returns:
        - float: The fitness value, between 0 and 1.
        """

    def eval_population(self, population: List[Genome]) -> float:
        """
        Evaluates the entire population's fitness.

        Parameters:
        - population (List[Genome]): A list of genome objects representing the population.
        
        Returns:
        - float: The average fitness of the population.
        """
        
    def select_parent(self, population: List[Genome]) -> Genome:
        """
        Selects a parent genome for crossover using a simple tournament selection method.

        Parameters:
        - population (List[Genome]): A list of genome objects from which a parent will be selected.
        
        Returns:
        - genome: The selected parent genome.
        """
        
    def crossover(self, parent1: Genome, parent2: Genome) -> Genome:
        """
        Performs crossover between two parent genomes to produce a child genome.

        Parameters:
        - parent1 (genome): The first parent genome.
        - parent2 (genome): The second parent genome.
        
        Returns:
        - genome: The child genome resulting from the crossover.
        """
        
    def mutate(genome: Genome, innovation_tracker):
        """
        Mutates a genome based on the mutation rate. 
        Each gene has a probability of being flipped.

        Parameters:
        - genome (genome): The genome to be mutated.
        
        Returns:
        - genome: The mutated genome.
        """

        # Filters the connections to only be the ones with inout then outputnode connected
        valid_connections = [connection for connection in Genome.connections 
                            if genome.nodes[conn.in_node].node_type == 'input' and 
                            genome.nodes[conn.out_node].node_type == 'output']

        connection_to_split = random.choice(valid_connections)
        
        # Create a new node
        new_node_id = len(genome.nodes)  # Assign the next available node ID
        new_node = Node(id=new_node_id, node_type='hidden')  # New node is a hidden node
        genome.nodes.append(new_node)


        # Create two new connections:
        # 1. Connection from the input node to the new node (with weight 1)
        innovation_number1 = innovation_tracker.get_innovation_number(connection_to_split.in_node, new_node_id)
        new_connection1 = Connection(
            in_node=connection_to_split.in_node,
            out_node=new_node_id,
            weight=1.0,  # Pass signal unchanged
            innovation_number=innovation_number1
        )

        # 2. Connection from the new node to the output node (with the original weight)
        innovation_number2 = innovation_tracker.get_innovation_number(new_node_id, connection_to_split.out_node)
        new_connection2 = Connection(
            in_node=new_node_id,
            out_node=connection_to_split.out_node,
            weight=connection_to_split.weight,  # Keep the original connection weight
            innovation_number=innovation_number2
        )

        # Add the new connections to the genome
        genome.connections.append(new_connection1)
        genome.connections.append(new_connection2)

    def evolve(self, population: List[Genome]) -> List[Genome]:
        """
        Evolves the population by performing selection, crossover, and mutation. The top-performing genomes are preserved
        """
