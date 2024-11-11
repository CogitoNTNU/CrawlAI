# src/genome.py

import random
from dataclasses import dataclass
from typing import List
from copy import deepcopy


class Innovation:
    __instance = None
    _global_innovation_counter = 0
    _innovation_history = {}

    @staticmethod
    def get_instance():
        if Innovation.__instance is None:
            Innovation()
        return Innovation.__instance

    def __init__(self):
        if Innovation.__instance is not None:
            raise Exception("This is a singleton.")
        else:
            Innovation.__instance = self

    def get_innovation_number(self, in_node, out_node):
        key = (in_node, out_node)
        if key in Innovation._innovation_history:
            return Innovation._innovation_history[key]
        else:
            Innovation._global_innovation_counter += 1
            Innovation._innovation_history[key] = Innovation._global_innovation_counter
            return Innovation._innovation_history[key]


@dataclass
class Node:
    id: int
    node_type: str  # 'input', 'hidden', 'output'

    def __hash__(self) -> int:
        return self.id


@dataclass
class Connection:
    in_node: int
    out_node: int
    weight: float
    innovation_number: int
    enabled: bool = True

    def change_enable(self, status: bool):
        self.enabled = status


class Genome:
    def __init__(self, genome_id: int, num_inputs: int = 0, num_outputs: int = 0):
        self.id = genome_id
        self.fitness: float = 0.0
        self.nodes: List[Node] = []
        self.connections: List[Connection] = []
        self.species: int = 0
        self.adjusted_fitness: float = 0.0
        self.innovation = Innovation.get_instance()

        # Store number of inputs and outputs
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

        # Create input nodes
        for i in range(num_inputs):
            node = Node(id=i, node_type="input")
            self.nodes.append(node)

        # Create output nodes
        for i in range(num_outputs):
            node = Node(id=num_inputs + i, node_type="output")
            self.nodes.append(node)

        # Connect each input node to each output node with a random weight
        input_nodes = [n for n in self.nodes if n.node_type == "input"]
        output_nodes = [n for n in self.nodes if n.node_type == "output"]
        for in_node in input_nodes:
            for out_node in output_nodes:
                innovation_number = self.innovation.get_innovation_number(
                    in_node.id, out_node.id
                )
                connection = Connection(
                    in_node=in_node.id,
                    out_node=out_node.id,
                    weight=random.uniform(-1.0, 1.0),
                    innovation_number=innovation_number,
                )
                self.connections.append(connection)

    def mutate_weights(self, delta: float = 0.1):
        """Mutate the weights of the connections."""
        for conn in self.connections:
            if random.random() < 0.1:
                conn.weight = random.uniform(-1.0, 1.0)
            else:
                conn.weight += random.gauss(0, delta)

    def mutate_connections(self):
        """Add a new connection between two nodes."""
        possible_in_nodes = list(self.nodes)
        possible_out_nodes = list(self.nodes)
        in_node = random.choice(possible_in_nodes)
        out_node = random.choice(possible_out_nodes)
        if in_node.id == out_node.id:
            return  # Avoid self-loops
        # Check if connection already exists
        for conn in self.connections:
            if conn.in_node == in_node.id and conn.out_node == out_node.id:
                return
        innovation_number = self.innovation.get_innovation_number(
            in_node.id, out_node.id
        )
        new_conn = Connection(
            in_node=in_node.id,
            out_node=out_node.id,
            weight=random.uniform(-1.0, 1.0),
            innovation_number=innovation_number,
        )
        self.connections.append(new_conn)

    def mutate_nodes(self):
        """Add a new node by splitting an existing connection."""
        if not self.connections:
            return
        con = random.choice(self.connections)
        if not con.enabled:
            return
        con.enabled = False
        new_node_id = max(node.id for node in self.nodes) + 1
        new_node = Node(id=new_node_id, node_type="hidden")
        self.nodes.append(new_node)

        innovation_number1 = self.innovation.get_innovation_number(
            con.in_node, new_node.id
        )
        innovation_number2 = self.innovation.get_innovation_number(
            new_node.id, con.out_node
        )

        con1 = Connection(
            in_node=con.in_node,
            out_node=new_node.id,
            weight=1.0,
            innovation_number=innovation_number1,
        )
        con2 = Connection(
            in_node=new_node.id,
            out_node=con.out_node,
            weight=con.weight,
            innovation_number=innovation_number2,
        )
        self.connections.append(con1)
        self.connections.append(con2)

    def mutate(self):
        """Apply mutations to the genome."""
        MUTATION_RATE_WEIGHT = 0.8
        MUTATION_RATE_CONNECTION = 0.05
        MUTATION_RATE_NODE = 0.03

        if random.random() < MUTATION_RATE_WEIGHT:
            self.mutate_weights(delta=0.1)
        if random.random() < MUTATION_RATE_CONNECTION:
            self.mutate_connections()
        if random.random() < MUTATION_RATE_NODE:
            self.mutate_nodes()

    def compute_compatibility_distance(self, other, c1=1.0, c2=1.0, c3=0.4) -> float:
        """Calculate the genetic distance (delta) between two genomes."""
        conn1 = {c.innovation_number: c for c in self.connections}
        conn2 = {c.innovation_number: c for c in other.connections}
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
                weight_difference_sum += abs(
                    conn1[innovation_number].weight - conn2[innovation_number].weight
                )
            elif innovation_number in conn1 or innovation_number in conn2:
                if innovation_number > max(max_innovation1, max_innovation2):
                    excess_genes += 1
                else:
                    disjoint_genes += 1

        average_weight_difference = (
            (weight_difference_sum / matching_genes) if matching_genes > 0 else 0
        )
        delta = (
            (c1 * excess_genes / N)
            + (c2 * disjoint_genes / N)
            + (c3 * average_weight_difference)
        )
        return delta

    def crossover(self, other):
        """Perform crossover between two genomes."""
        # Assume self is the more fit parent
        child = Genome(
            genome_id=-1,  # Temporary ID
            num_inputs=self.num_inputs,
            num_outputs=self.num_outputs,
        )
        child.nodes = deepcopy(self.nodes)
        # Ensure all nodes from other are present
        for node in other.nodes:
            if node.id not in [n.id for n in child.nodes]:
                child.nodes.append(deepcopy(node))

        # Inherit connections
        self_conn_dict = {conn.innovation_number: conn for conn in self.connections}
        other_conn_dict = {conn.innovation_number: conn for conn in other.connections}

        for innovation_number in set(self_conn_dict.keys()).union(
            other_conn_dict.keys()
        ):
            conn = None
            if (
                innovation_number in self_conn_dict
                and innovation_number in other_conn_dict
            ):
                # Matching genes - randomly choose
                if random.random() < 0.5:
                    conn = deepcopy(self_conn_dict[innovation_number])
                else:
                    conn = deepcopy(other_conn_dict[innovation_number])
            elif innovation_number in self_conn_dict:
                # Excess or disjoint genes from the more fit parent
                conn = deepcopy(self_conn_dict[innovation_number])
            else:
                # Excess or disjoint genes from the other parent
                conn = deepcopy(other_conn_dict[innovation_number])

            if conn:
                child.connections.append(conn)

        return child

    def copy(self):
        """Create a deep copy of the genome."""
        new_genome = Genome(
            genome_id=self.id, num_inputs=self.num_inputs, num_outputs=self.num_outputs
        )
        new_genome.nodes = deepcopy(self.nodes)
        new_genome.connections = deepcopy(self.connections)
        new_genome.fitness = self.fitness
        new_genome.adjusted_fitness = self.adjusted_fitness
        new_genome.species = self.species
        return new_genome

    def __str__(self):
        return f"Genome ID: {self.id}, Fitness: {self.fitness}, Species: {self.species}, Adjusted Fitness: {self.adjusted_fitness}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.fitness < other.fitness
