import os
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

# --------- General/Portable Setup ---------
GRAPH_NAME = input("Enter the Graph Name: ").strip()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
surgery_folder = os.path.join(BASE_DIR, 'output_graphs', GRAPH_NAME, 'surgery')
image_folder = os.path.join(BASE_DIR, 'frames_cuts')
os.makedirs(image_folder, exist_ok=True)

# --------- Find all cut_*.gexf files ---------
cut_files = [f for f in os.listdir(surgery_folder) if f.startswith('cut_') and f.endswith('.gexf')]
cut_files = sorted(cut_files, key=lambda x: int(x.split('_')[1].split('.')[0]))  # Sort numerically

# --------- Fixed Position Layout from input graph ---------
input_graph_path = os.path.join(BASE_DIR, 'input_graphs', f'{GRAPH_NAME}.gml')
input_graph = nx.read_gml(input_graph_path, label=None)
fixed_pos = nx.kamada_kawai_layout(input_graph)
fixed_pos = {str(k): v for k, v in fixed_pos.items()}
# Flip the layout horizontally (mirror left/right)
fixed_pos = {k: (-v[0], v[1]) for k, v in fixed_pos.items()}
# --------- Precompute global min/max weights ---------
global_min_w = float('inf')
global_max_w = float('-inf')
for cut_file in cut_files:
    g = nx.read_gexf(os.path.join(surgery_folder, cut_file))
    weights = [float(g[u][v].get('weight', 1.0)) for u, v in g.edges()]
    if weights:
        global_min_w = min(global_min_w, min(weights))
        global_max_w = max(global_max_w, max(weights))

min_width = 2
max_width = 10

# --------- Draw each cut and save frame ---------
for i, cut_file in enumerate(cut_files):
    g = nx.read_gexf(os.path.join(surgery_folder, cut_file))
    plt.figure(figsize=(8, 6))
    pos = fixed_pos

    weights = [float(g[u][v].get('weight', 1.0)) for u, v in g.edges()]
    norm_weights = [
        min_width + (max_width - min_width) * (w - global_min_w) / (global_max_w - global_min_w) if global_max_w > global_min_w else min_width
        for w in weights
    ]

    nx.draw_networkx_nodes(g, pos, node_size=300, node_color='black')
    nx.draw_networkx_edges(g, pos, edge_color='black', width=norm_weights)
    nx.draw_networkx_labels(g, pos, font_color='white', font_size=10)  # Node labels in white for contrast
    # (No edge labels)
    plt.title(f"Cut Step {i}")
    plt.axis('off')
    frame_path = os.path.join(image_folder, f"cut_frame_{i:03d}.png")
    plt.savefig(frame_path, bbox_inches='tight')
    plt.close()

# --------- Create GIF ---------
frames = [Image.open(os.path.join(image_folder, f)) for f in sorted(os.listdir(image_folder)) if f.endswith('.png')]
pause_frames = 250
frames.extend([frames[-1]] * pause_frames)
frames[0].save(
    f'{GRAPH_NAME}_cuts.gif',
    format='GIF',
    append_images=frames[1:],
    save_all=True,
    duration=1500,  # Each frame lasts 1.5 seconds
    loop=0
)