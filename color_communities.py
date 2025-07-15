import networkx as nx
import random
from networkx.algorithms.community import greedy_modularity_communities

# Load the final graph
g = nx.read_gexf('output_graphs/round_counter/surgery/best_cut.gexf')

# Detect communities (using greedy modularity)
communities = list(greedy_modularity_communities(g.to_undirected()))

# Assign a random color to each community
def random_rgb():
    return {'r': random.randint(0,255), 'g': random.randint(0,255), 'b': random.randint(0,255)}

community_colors = [random_rgb() for _ in communities]

# Assign color to each node based on its community
for idx, comm in enumerate(communities):
    for node in comm:
        g.nodes[node]['viz'] = {'color': community_colors[idx]}

# Save the colored graph
nx.write_gexf(g, 'output_graphs/round_counter/best_colored.gexf')