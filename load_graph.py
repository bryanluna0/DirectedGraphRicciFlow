import networkx as nx
import os

class DiGraph:
    def __init__(self, graph_file):
        self.G = nx.read_gml(os.path.join("input_graphs", graph_file)) 
        n_edges = len(self.G.edges())
        weight = {e: 1.0 for e in self.G.edges()}
        nx.set_edge_attributes(self.G, weight, 'weight')
        print("Data loaded. \nNumber of nodes： {}\nNumber of edges: {}".format(self.G.number_of_nodes(), self.G.number_of_edges()))
        
