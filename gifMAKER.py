import os
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

# Folders
gexf_folder = '/Users/andrescorrea/Documents/GitHub/DirectedGraphRicciFlow/output_graphs/round_counter'
image_folder = 'frames'
os.makedirs(image_folder, exist_ok=True)

# Build ordered list: origin.gexf, 0.gexf ... N.gexf, best.gexf
gexf_files = []
if 'origin.gexf' in os.listdir(gexf_folder):
    gexf_files.append('origin.gexf')
numbered = [f for f in os.listdir(gexf_folder) if f.endswith('.gexf') and f[:-5].isdigit()]
gexf_files += sorted(numbered, key=lambda x: int(x[:-5]))
if 'best.gexf' in os.listdir(gexf_folder):
    gexf_files.append('best.gexf')

# Generate PNGs from GEXF files
for i, gexf_file in enumerate(gexf_files):
    g = nx.read_gexf(os.path.join(gexf_folder, gexf_file))
    
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(g, seed=42)  # consistent layout

    # Get edge weights for thickness
    weights = [float(g[u][v].get('weight', 1.0)) for u, v in g.edges()]
    min_w, max_w = min(weights), max(weights)
    norm_weights = [1 + 4 * (w - min_w) / (max_w - min_w) if max_w > min_w else 2 for w in weights]

    nx.draw_networkx_nodes(g, pos, node_size=50, node_color='blue')
    nx.draw_networkx_edges(g, pos, edge_color='black', width=norm_weights)
    nx.draw_networkx_edge_labels(
        g, pos,
        edge_labels={(u, v): f"{g[u][v].get('weight', 1.0):.2f}" for u, v in g.edges()},
        font_size=6
    )
    
    frame_path = os.path.join(image_folder, f"frame_{i:03d}.png")
    plt.axis('off')
    plt.savefig(frame_path, bbox_inches='tight')
    plt.close()

# Create GIF
frames = [Image.open(os.path.join(image_folder, f)) for f in sorted(os.listdir(image_folder)) if f.endswith('.png')]

# Repeat the last frame to pause at the end
pause_frames = 100  # Number of times to repeat the last frame
frames.extend([frames[-1]] * pause_frames)

# Save GIF with slower frame rate (duration in ms)
frames[0].save(
    'output_graph.gif',
    format='GIF',
    append_images=frames[1:],
    save_all=True,
    duration=500,  # 500 ms per frame (slower)
    loop=0
)