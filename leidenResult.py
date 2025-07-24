import igraph as ig
import leidenalg
import os

# === Load directed graph from GML ===
graph_path = os.path.join("input_graphs", "round_counter.gml")
g = ig.Graph.Read_GML(graph_path)
g.to_directed()  # Ensure it's treated as directed

# === Run Leiden algorithm ===
partition = leidenalg.find_partition(
    g, 
    leidenalg.ModularityVertexPartition, 
    weights=g.es["weight"] if "weight" in g.edge_attributes() else None
)

# === Print community information ===
print(f"Number of communities: {len(partition)}")
for i, community in enumerate(partition):
    print(f"Community {i+1}: {community}")

# === Save each community as its own subgraph ===
output_dir = "leiden_communities"
os.makedirs(output_dir, exist_ok=True)

for i, community in enumerate(partition):
    subgraph = g.subgraph(community)
    subgraph_file = os.path.join(output_dir, f"community_{i+1}.gml")
    subgraph.write_gml(subgraph_file)

print(f"Saved {len(partition)} community subgraphs to '{output_dir}' directory.")
