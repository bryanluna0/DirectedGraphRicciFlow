import os
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
import random
from color_communities import color_communities


# --------- General/Portable Setup ---------
GRAPH_NAME = input("Enter the Graph Name:").strip()  # Change this to use a different graph

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
gexf_folder = os.path.join(BASE_DIR, 'output_graphs', GRAPH_NAME)
image_folder = os.path.join(BASE_DIR, 'frames')
os.makedirs(image_folder, exist_ok=True)

# Build ordered list: origin.gexf, 0.gexf ... N.gexf, best_colored.gexf
gexf_files = []
if 'origin.gexf' in os.listdir(gexf_folder):
    gexf_files.append('origin.gexf')
numbered = [f for f in os.listdir(gexf_folder) if f.endswith('.gexf') and f[:-5].isdigit()]
gexf_files += sorted(numbered, key=lambda x: int(x[:-5]))
if 'best_colored.gexf' in os.listdir(gexf_folder):
    gexf_files.append('best_colored.gexf')

# --------- Fixed Position Layout ---------
input_graph_path = os.path.join(BASE_DIR, 'input_graphs', f'{GRAPH_NAME}.gml')
input_graph = nx.read_gml(input_graph_path, label=None)
fixed_pos = nx.kamada_kawai_layout(input_graph)
fixed_pos = {str(k): v for k, v in fixed_pos.items()}

# --------- Precompute global min/max weights ---------
global_min_w = float('inf')
global_max_w = float('-inf')
for gexf_file in gexf_files:
    g = nx.read_gexf(os.path.join(gexf_folder, gexf_file))
    weights = [float(g[u][v].get('weight', 1.0)) for u, v in g.edges()]
    if weights:
        global_min_w = min(global_min_w, min(weights))
        global_max_w = max(global_max_w, max(weights))

min_width = 1
max_width = 15

for i, gexf_file in enumerate(gexf_files):
    g = nx.read_gexf(os.path.join(gexf_folder, gexf_file))
    plt.figure(figsize=(8, 6))
    pos = fixed_pos  # Use fixed positions

    weights = [float(g[u][v].get('weight', 1.0)) for u, v in g.edges()]
    norm_weights = [
        min_width + (max_width - min_width) * (w - global_min_w) / (global_max_w - global_min_w) if global_max_w > global_min_w else min_width
        for w in weights
    ]

    # For the last frame, color communities
    if i == len(gexf_files) - 1:
        from networkx.algorithms.community import greedy_modularity_communities
        communities = list(greedy_modularity_communities(g.to_undirected()))
        colors = []
        for _ in communities:
            colors.append([random.random(), random.random(), random.random()])
        node_color_map = {}
        for idx, comm in enumerate(communities):
            for node in comm:
                node_color_map[node] = colors[idx]
        node_colors = [node_color_map[n] for n in g.nodes()]
    else:
        node_colors = 'blue'

    nx.draw_networkx_nodes(g, pos, node_size=50, node_color=node_colors)
    nx.draw_networkx_edges(g, pos, edge_color='black', width=norm_weights)
    nx.draw_networkx_edge_labels(
        g, pos,
        edge_labels={(u, v): f"{g[u][v].get('weight', 1.0):.2f}" for u, v in g.edges()},
        font_size=6
    )
    frame_path = os.path.join(image_folder, f"frame_{i:03d}.png")
    if(i<=len(gexf_files) - 1 and gexf_file != 'best_colored.gexf'):
        plt.title(f"Ricci Flow Iteration {i}")
    else:
        plt.title(f"Post Surgery") 

    plt.axis('off')
    plt.savefig(frame_path, bbox_inches='tight')
    plt.close()

color_communities(GRAPH_NAME)

# Create GIF
frames = [Image.open(os.path.join(image_folder, f)) for f in sorted(os.listdir(image_folder)) if f.endswith('.png')]
pause_frames = 100
frames.extend([frames[-1]] * pause_frames)
frames[0].save(
    'output_graph.gif',
    format='GIF',
    append_images=frames[1:],
    save_all=True,
    duration=500,
    loop=0
)