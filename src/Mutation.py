

from src.genome import Genome, Node, Connection, Inovation
import random


class Mutation():

    def __init__(self,genome: Genome):
        self.genome = genome


    def weight_mutation(self, delta: float):

        for conn in self.genome.connections:
        # Small chance to fully reset the weight to a random value
            
            if random.random() < 0.1:  # 10% chance to completely change the weight
                conn.weight = random.uniform(-1.0, 1.0)  # Reset weight to random value
            else:
            # Perturb the weight slightly (Gaussian perturbation)
                conn.weight += random.gauss(0, delta)  # Random perturbation with mean 0 and standard deviation delta


    def connection_mutation(self):

        nodes = self.genome.nodes
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
        
        self.genome.connections.append(new_conn)


    def node_mutation(self):
        new_node = Node(len(self.genome.nodes)+1, "hidden")
        con = random.choice(self.genome.connections)
        con.change_enable(False)

        con1 = Connection(con.in_node_id, new_node, 1.0, True, Inovation.get_instance()._get_innovation_number(con.in_node_id, new_node))
        con2 = Connection(new_node,con.out_node_id,  con.weight, True, Inovation.get_instance()._get_innovation_number(new_node,con.out_node_id,))

        self.genome.connections.append(con1)
        self.genome.connections.append(con2)

        self.genome.nodes.append(new_node)



        







    





    