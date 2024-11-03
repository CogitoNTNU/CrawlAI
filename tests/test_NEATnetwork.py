

from ..src.genome import Node, Connection, Genome
from src.NEATnetwork import NEATNetwork



def test_NEAT_network():

    node_1 = Node(1,"input")
    node_2 = Node(2,"input")          
    node_3 = Node(3,"input")
    node_4 = Node(4,"hidden")          
    node_5 = Node(5,"output")     

   
    nodes_list = [node_1,node_2,node_3,node_4,node_5]


    con_1 = Connection(node_1, node_4, 0.7, True, 1)
    con_2 = Connection(node_2, node_4, 0.7, True, 2)      
    con_3 = Connection(node_3, node_4, 0.5, True, 3)      
    con_4 = Connection(node_2, node_5, 0.2, True, 4)      
    con_5 = Connection(node_5, node_4, 0.4, True, 5)      
    con_6 = Connection(node_1, node_5, 0.6, False, 6)      
    con_7 = Connection(node_1, node_5, 0.6, True, 11) 


    conns= [con_1,con_2,con_3,con_4,con_5,con_6,con_7]


    genome = Genome(id = 1,nodes = nodes_list,connections = conns)


    assert NEATNetwork(genome = genome) == 1.52                    