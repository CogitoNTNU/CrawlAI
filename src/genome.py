
import random
from dataclasses import dataclass, field  # Ensure field is imported
from typing import List, Optional

@dataclass
class Node:
    """Node in the neural network, representing a neuron."""
    id: int
    node_type: str  # 'input', 'hidden', 'output'

@dataclass
class Connection:
    """Represents a connection between two nodes in the network."""
    in_node: int  
    out_node: int
    weight: float
    enabled: bool = True   #If there is an edge between the nodes
    innovation_number: Optional[int] = None  # For tracking mutations uniquely



@dataclass
class Genome:
    """Genome class representing a neural network in NEAT."""
    id: int
    fitness: float = 0.0
    nodes: List[Node] = field(default_factory=list)  # Use field for default empty lists
    connections: List[Connection] = field(default_factory=list)
    species: int = 0
    adjusted_fitness: float = 0.0


    def __str__(self):
        return f"Genome ID: {self.id}, Fitness: {self.fitness}, Species: {self.species}, Adjusted Fitness: {self.adjusted_fitness}"

    def __repr__(self):
        return f"Genome ID: {self.id}, Fitness: {self.fitness}, Species: {self.species}, Adjusted Fitness: {self.adjusted_fitness}"

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.fitness < other.fitness


def create_initial_genome(genome_id: int, num_inputs: int, num_outputs: int) -> Genome:
    """Create an initial genome with specified input and output nodes."""

    nodes = []
    connections = []
    
    # Create input nodes
    for i in range(num_inputs):
        nodes.append(Node(id=i, node_type='input'))
    
    # Create output nodes
    for i in range(num_outputs):
        nodes.append(Node(id=num_inputs + i, node_type='output'))
    
    # Connect each input node to each output node with a random weight
    
    inn_num = 0

    for input_node in range(num_inputs):
        for output_node in range(num_outputs):
            connections.append(Connection(
                in_node=input_node,
                out_node=num_inputs + output_node,
                weight=random.uniform(-1.0, 1.0),  # Random weight between -1 and 1
                innovation_number= inn_num  # You'd manage innovation numbers uniquely in a full NEAT implementation
            ))
        inn_num += 1
    
    return Genome(id=genome_id, nodes=nodes, connections=connections)


def initialize_population(pop_size: int, num_inputs: int, num_outputs: int) -> List[Genome]:
    """Initialize a population of genomes."""
    population = []
    for genome_id in range(pop_size):
        genome = create_initial_genome(genome_id, num_inputs, num_outputs)
        population.append(genome)
    return population


# Example usage:
if __name__ == "__main__":
    # Initialize a population of genomes for a NEAT algorithm
    population_size = 10
    num_input_nodes = 3  # For example, 3 input nodes
    num_output_nodes = 1  # For example, 1 output node

    population = initialize_population(population_size, num_input_nodes, num_output_nodes)
    
    # Print the initialized genomes
    for genome in population:
        print(genome)

