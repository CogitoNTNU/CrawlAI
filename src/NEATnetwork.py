import torch
import torch.nn as nn
from genome import Genome
from collections import defaultdict, deque

class NEATNetwork(nn.Module):
    def __init__(self, genome: Genome):
        super(NEATNetwork, self).__init__()
        
        # Store genome information
        self.genome = genome
        
        # Create dictionaries for nodes and connections
        self.node_dict = {node.id: node for node in genome.nodes}
        self.connection_dict = {conn.innovation_number: conn for conn in genome.connections if conn.enabled}

        # Create parameter lists for weights
        self.connections = nn.ParameterDict({
            f"{conn.in_node}->{conn.out_node}": nn.Parameter(torch.tensor(conn.weight, dtype=torch.float32))
            for conn in genome.connections if conn.enabled
        })

        # Topologically sort nodes based on connections
        self.topological_order = self._topological_sort()

    def _topological_sort(self):
        """Performs topological sorting on the nodes based on their connections."""
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

    def forward(self, x):
        # Dictionary to store outputs of each node
        node_outputs = {}

        # Assume input nodes are provided in the correct order
        input_nodes = [node for node in self.genome.nodes if node.node_type == 'input']
        output_nodes = [node for node in self.genome.nodes if node.node_type == 'output']

        # Assign input values
        for i, node in enumerate(input_nodes):
            node_outputs[node.id] = x[:, i]

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
                weight = self.connections[f"{in_node}->{conn.out_node}"]
                node_sum += node_outputs[in_node] * weight

            # Apply activation (sigmoid for hidden and output nodes)
            node_outputs[node_id] = torch.sigmoid(node_sum)

        # Collect the outputs for final output nodes
        output = torch.stack([node_outputs[node.id] for node in output_nodes], dim=1)
        return output

# Example usage:
# genome = Genome(...) # Your genome definition
# model = NEATNetwork(genome)
# x = torch.rand(1, len([n for n in genome.nodes if n.node_type == 'input']))  # Random input
# output = model(x)
