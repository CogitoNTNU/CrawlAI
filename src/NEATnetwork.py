from src.genome import Genome
from collections import defaultdict, deque
import numpy as np


class NEATNetwork():

    def __init__(self, genome: Genome):
        
        # Store genome information
        self.genome = genome
        
        # Create dictionaries for nodes and connections
        self.node_dict = {node.id: node for node in genome.nodes}
        self.connection_dict = {conn.innovation_number: conn for conn in genome.connections if conn.enabled}
        
        # Topologically sort nodes based on connections
        self.topological_order = self._topological_sort()

    def sigmoid(self, x: np.ndarray) -> np.ndarray:
        """ Sigmoid activation function.

        Args:
            x (np.ndarray): Input array

        Returns:
            np.ndarray: Output array after applying sigmoid function
        """
        return 1 / (1 + np.exp(-x))

    def ReLU(self, x):
        return np.maximum(0, x)

    def _topological_sort(self) -> list:
        """
        Performs topological sorting on the nodes based on their connections.
        """
        in_degree = defaultdict(int)
        adjacency_list = defaultdict(list)

        # Build graph
        for conn in self.genome.connections:
            if conn.enabled:
                adjacency_list[conn.in_node].append(conn.out_node)
                in_degree[conn.out_node] += 1

        # Initialize the queue with input nodes (no incoming connections)
        queue = deque([node.id for node in self.genome.nodes if in_degree[node.id] == 0])

        topological_order = []
        while queue:
            node = queue.popleft()
            topological_order.append(node)

            # Process the neighbors of this node
            for neighbor in adjacency_list[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return topological_order

    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Perform a forward pass through the network given an input.
        Args:
            x: Input array to the network
        Returns:
            Output array from the network
        """
        # Dictionary to store outputs of each node
        node_outputs = {}

        # Assume input nodes are provided in the correct order
        input_nodes = [node for node in self.genome.nodes if node.node_type == 'input']
        output_nodes = [node for node in self.genome.nodes if node.node_type == 'output']

        # Assign input values
        for i, node in enumerate(input_nodes):
            node_outputs[node.id] = x[i]

        # Process nodes in topological order
        for node_id in self.topological_order:
            # Skip input nodes, their values are already set
            if node_id in node_outputs:
                continue

            # Compute the value of this node based on incoming connections
            incoming_connections = [conn for conn in self.genome.connections if conn.out_node == node_id and conn.enabled]

            node_sum = 0
            for conn in incoming_connections:
                in_node = conn.in_node
                weight = conn.weight
                node_sum += node_outputs[in_node] * weight
                node_sum = node_sum/50 # Random shit because sum is not normalized
            # Apply activation (sigmoid for hidden and output nodes)
            node_outputs[node_id] = self.ReLU(node_sum)

        # Collect the outputs for final output nodes
        output = np.array([node_outputs[node.id] for node in output_nodes])
        return output

