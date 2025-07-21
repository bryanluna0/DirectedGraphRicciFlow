import networkx as nx
import random
from networkx.algorithms.community import greedy_modularity_communities

def color_communities(graph_name):
    # Build the path using the graph name
    best_cut_path = f'output_graphs/{graph_name}/surgery/best_cut.gexf'
    best_colored_path = f'output_graphs/{graph_name}/best_colored.gexf'

    # Read the best_cut graph
    g = nx.read_gexf(best_cut_path)
    # Find communities using greedy modularity
    communities = list(greedy_modularity_communities(g.to_undirected()))

    # Helper to generate a random RGB color
    def random_rgb():
        return {'r': random.randint(0,255), 'g': random.randint(0,255), 'b': random.randint(0,255)}

    # Assign a random color to each community
    community_colors = [random_rgb() for _ in communities]

    # Color each node according to its community
    for idx, comm in enumerate(communities):
        for node in comm:
            g.nodes[node]['viz'] = {'color': community_colors[idx]}

    # Save the colored graph
    nx.write_gexf(g, best_colored_path)