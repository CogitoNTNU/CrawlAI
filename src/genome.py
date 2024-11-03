import random
from dataclasses import dataclass
from typing import List 


class Inovation:
    __instance = None
    _global_innovation_counter = 0
    _innovation_history = {}

    @staticmethod
    def get_instance():
        if Inovation.__instance is None:
            Inovation()
        return Inovation.__instance

    def __init__(self):
        if Inovation.__instance is not None:
            raise Exception("This is a singleton.")
        else:
            Inovation.__instance = self

    @staticmethod
    def _get_innovation_number(in_node, out_node):
        key = (in_node, out_node)
        if key in Inovation._innovation_history:
            return Inovation._innovation_history[key]
        else:
            Inovation._global_innovation_counter += 1
            Inovation._innovation_history[key] =\
                Inovation._global_innovation_counter
            return Inovation._innovation_history[key]


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
    enabled: bool = True
    innovation_number: int

    def change_enable(self, status: bool):
        self.enabled = status
        

class Genome:
    def __init__(self, genome_id: int, num_inputs: int, num_outputs: int):
        self.id = genome_id
        self.fitness: float = 0.0
        self.nodes: List[Node] = []
        self.connections: List[Connection] = []
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
                    weight=random.uniform(-1.0, 1.0),
                    innovation_number=Inovation.get_instance()._get_innovation_number(
                        input_node,
                        num_inputs + output_node
                    )
                ))

    def mutate_weights(self, delta: float):
        for conn in self.connections:
            if random.random() < 0.1:
                conn.weight = random.uniform(-1.0, 1.0)
            else:
                conn.weight += random.gauss(0, delta)

    def mutate_connections(self):
        in_node = random.choice(self.nodes)
        out_node = random.choice(self.nodes)
        weight = random.uniform(-1.0, 1.0)
        enabled = random.choice([True, False])
        new_conn = Connection(
            in_node.id,
            out_node.id,
            weight,
            enabled,
            Inovation.get_instance()._get_innovation_number(
                in_node.id, 
                out_node.id)
        )
        self.connections.append(new_conn)

    def mutate_nodes(self):
        new_node = Node(len(self.nodes), "hidden")
        con = random.choice(self.connections)
        con.change_enable(False)

        con1 = Connection(
            con.in_node, 
            new_node.id, 
            1.0, 
            True, 
            Inovation.get_instance()._get_innovation_number(con.in_node, new_node.id))
        con2 = Connection(
            new_node.id, 
            con.out_node, 
            con.weight, 
            True, 
            Inovation.get_instance()._get_innovation_number(new_node.id, con.out_node))

        self.connections.extend([con1, con2])
        self.nodes.append(new_node)

    def __str__(self):
        return f"Genome ID: {self.id}, Fitness: {self.fitness}, Species: {self.species}, Adjusted Fitness: {self.adjusted_fitness}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.fitness < other.fitness