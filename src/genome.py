import random
from dataclasses import dataclass, field  # Ensure field is imported
from typing import List, Optional


class Inovation:
    __instance = None

    _global_innovation_counter = 0
    _innovation_history = {}  # This will track (in_node, out_node) -> innovation_number

    @staticmethod
    def get_instance():
        if Inovation.__instance == None:
            Inovation()
        return Inovation.__instance

    def __init__(self):
        if self.__instance is not None:
            raise Exception("This is a singleton.")
        else:
            Inovation.__instance = self

    def _get_innovation_number(self,in_node,out_node):
        
        key = (in_node, out_node)
        if key in self._innovation_history:
            return self._innovation_history[key]
        else:
            self._global_innovation_counter += 1
            self._innovation_history[(in_node,out_node)] = self._global_innovation_counter
            return self._innovation_history[(in_node,out_node)]
        
    



    
        
        
            
@dataclass
class Node:
    """Node in the neural network, representing a neuron."""

    id: int
    node_type: str  # 'input', 'hidden', 'output'

    def __hash__(self) -> int:
        return self.id

@dataclass
class Connection:
    """Represents a connection between two nodes in the network."""
    in_node: int  
    out_node: int
    weight: float
    enabled: bool = True   #If there is an edge between the nodes
    innovation_number: int 

class Genome:
    """Genome class representing a neural network in NEAT."""
    id: int
    fitness: float = 0.0
    nodes: set[Node] = field(default_factory=set)  # Use field for default empty lists
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


def get_innovation_number(in_node, out_node):   # Method that gets or sets innovation number
    global global_innovation_counter
    global innovation_history

    if (in_node, out_node) in innovation_history:
        return innovation_history[(in_node, out_node)]
    else:
        global_innovation_counter += 1
        innovation_history[(in_node, out_node)] = global_innovation_counter
        return global_innovation_counter


def create_initial_genome(genome_id: int, num_inputs: int, num_outputs: int) -> Genome:
    """Create an initial genome with specified input and output nodes."""

    nodes = set()  # Initialize nodes as a set to match Genome class
    connections = []
    
    # Create input nodes
    for i in range(num_inputs):
        nodes.add(Node(id=i, node_type='input'))
    
    # Create output nodes
    for i in range(num_outputs):
        nodes.add(Node(id=num_inputs + i, node_type='output'))
    
    # Connect each input node to each output node with a random weight
    for input_node in range(num_inputs):
        for output_node in range(num_outputs):
            connections.append(Connection(
                in_node = input_node,
                out_node = num_inputs + output_node,
                weight = random.uniform(-1.0, 1.0),  # Random weight between -1 and 1
                innovation_number = get_innovation_number(input_node, num_inputs + output_node)
            ))
    
    return Genome(id = genome_id, nodes = nodes, connections=connections)


def initialize_population(pop_size: int, num_inputs: int, num_outputs: int) -> List[Genome]:
    """Initialize a population of genomes."""
    population = []
    for genome_id in range(pop_size):
        genome = create_initial_genome(genome_id, num_inputs, num_outputs)
        population.append(genome)
    return population



def translate_genome_to_network(genome: Genome):
    
    input_nodes = []
    hidden_nodes = [] 
    output_nodes = [] 
    connections = []


    for node in genome.nodes:
        if node.node_type == "input":
            input_nodes.append(node)
        elif node.node_type == "hidden":
            hidden_nodes.append(node)
        elif node.node_type == "output":
            output_nodes.append(node)


    for connection in genome.connections:
        if connection.enabled:
            connections.append((connection.in_node,connection.out_node,connection.weight))


    network = {
    'input_nodes': input_nodes,
    'hidden_nodes': hidden_nodes,
    'output_nodes': output_nodes,
    'connections': connections

    }
    
    return network

        


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

