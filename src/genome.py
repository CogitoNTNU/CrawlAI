import random
from dataclasses import dataclass, field  # Ensure field is imported
from typing import List


class Inovation:
    __instance = None

    _global_innovation_counter = 0
    # This will track (in_node, out_node) -> innovation_number
    _innovation_history = {} 

    @staticmethod
    def get_instance():
        if Inovation.__instance is None:
            Inovation()
        return Inovation.__instance

    def __init__(self):
        if self.__instance is not None:
            raise Exception("This is a singleton.")
        else:
            Inovation.__instance = self

    def _get_innovation_number(self, in_node, out_node):
        
        key = (in_node, out_node)
        if key in self._innovation_history:
            return self._innovation_history[key]
        else:
            self._global_innovation_counter += 1
            self._innovation_history[(in_node, out_node)] = \
                self._global_innovation_counter
            return self._innovation_history[(in_node, out_node)]
          
            
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
    enabled: bool = True   # If there is an edge between the nodes
    innovation_number: int 


class Genome:
    """Genome class representing a neural network in NEAT."""
    id: int 
    fitness: float
    nodes: List[Node]
    connections: List[Connection]
    species: int
    adjusted_fitness: float
    
    def __init__(self, genome_id: int, num_inputs: int, num_outputs: int):
        """Create an initial genome with specified input and output nodes."""
        self.id = genome_id
        self.fitness: float = 0.0
        self.nodes: List[Node] = field(default_factory=list)
        self.connections: List[Connection] = field(default_factory=list)
        self.species: int = 0
        self.adjusted_fitness: float = 0.0

        # Create input nodes
        for i in range(num_inputs):
            self.nodes.append(Node(id=i, node_type='input'))
        
        # Create output nodes
        for i in range(num_outputs):
            self.nodes.append(Node(id=num_inputs + i, node_type='output'))
        
        # Connect each input node to each output node with a random weight
        for input_node in range(num_inputs):
            for output_node in range(num_outputs):
                self.connections.append(Connection(
                    in_node=input_node,
                    out_node=num_inputs + output_node,
                    # Random weight between -1 and 1
                    weight=random.uniform(-1.0, 1.0),  
                    innovation_number=get_innovation_number(
                        input_node, 
                        num_inputs + output_node)
                )) 
    
    def mutate_weights(self, delta: float):

        for conn in self.connections:
        # Small chance to fully reset the weight to a random value
            if random.random() < 0.1:  # 10% chance to completely change the weight
                conn.weight = random.uniform(-1.0, 1.0)  # Reset weight to random value
            else:
            # Perturb the weight slightly (Gaussian perturbation)
                conn.weight += random.gauss(0, delta)  # Random perturbation with mean 0 and standard deviation delta

    def mutate_connections(self):

        nodes = self.nodes

        in_node = random.choice(nodes)
        out_node = random.choice(nodes)
        weight = random.uniform(-1.0,1-0)
        enabled = random.choice([True,False])
        new_conn = Connection(
            in_node,
            out_node,
            weight,
            enabled,
            Inovation.get_instance()._get_innovation_number(in_node,out_node))
        
        self.connections.append(new_conn)
    
    def mutate_nodes(self):
        new_node = Node(len(self.nodes)+1, "hidden")
        con = random.choice(self.connections)
        con.change_enable(False)

        con1 = Connection(con.in_node_id, new_node, 1.0, True, Inovation.get_instance()._get_innovation_number(con.in_node_id, new_node))
        con2 = Connection(new_node,con.out_node_id,  con.weight, True, Inovation.get_instance()._get_innovation_number(new_node,con.out_node_id,))

        self.connections.append(con1)
        self.connections.append(con2)

        self.nodes.append(new_node)


    def __str__(self):
        return f"Genome ID: {self.id}, Fitness: {self.fitness},"
        f"Species: {self.species}, Adjusted Fitness: {self.adjusted_fitness}"

    def __repr__(self):
        return f"Genome ID: {self.id}, Fitness: {self.fitness},"
        f"Species: {self.species}, Adjusted Fitness: {self.adjusted_fitness}"

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.fitness < other.fitness


def get_innovation_number(in_node, out_node): 
    """
    Method that gets or sets innovation number for a 
    connection between two nodes.

    Args:
        in_node (_type_)
        out_node (_type_)

    Returns:
        _type_: global_innovation_counter
    """
    global global_innovation_counter
    global innovation_history

    if (in_node, out_node) in innovation_history:
        return innovation_history[(in_node, out_node)]
    else:
        global_innovation_counter += 1
        innovation_history[(in_node, out_node)] = global_innovation_counter
        return global_innovation_counter


def initialize_population(
        pop_size: int,
        num_inputs: int,
        num_outputs: int
        ) -> List[Genome]:
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

    population = initialize_population(
        population_size,
        num_input_nodes,
        num_output_nodes)
    
    # Print the initialized genomes
    for genome in population:
        print(genome)

