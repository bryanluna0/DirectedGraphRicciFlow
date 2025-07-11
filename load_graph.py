import networkx as nx
import os

class DiGraph:
    def __init__(self, graph_file):
        self.name = graph_file[0:-4]
        self.G = nx.read_gml(os.path.join("input_graphs", graph_file), label=None)
        self.G.graph['name'] = self.name
        n_edges = len(self.G.edges())
        weight = {e: 1.0 for e in self.G.edges()}
        nx.set_edge_attributes(self.G, weight, 'weight')
        print("Data loaded. \nNumber of nodes： {}\nNumber of edges: {}".format(self.G.number_of_nodes(), self.G.number_of_edges()))
