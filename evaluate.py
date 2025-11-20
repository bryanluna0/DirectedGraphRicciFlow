import igraph as ig
import leidenalg
import os
import networkx as nx
import pandas as pd
import numpy as np

def leiden_communities():
    # === Load directed graph from GML ===
    graph_path = os.path.join("input_graphs", "SampleGraph2.gml")
    g = ig.Graph.Read_GML(graph_path)
    g.to_directed()  # Ensure it's treated as directed

    print(g)
    # === Run Leiden algorithm ===
    partition = leidenalg.find_partition(
        g, 
        leidenalg.ModularityVertexPartition, 
        weights=g.es["weight"] if "weight" in g.edge_attributes() else None
    )

    # Convert igraph indices to node labels
    node_labels = g.vs["label"] if "label" in g.vs.attributes() else list(range(g.vcount()))
    leiden_communities = []
    for community in partition:
        leiden_communities.append([node_labels[i] for i in community])
        # === Print community information ===
    # === Print community information ===
    print(f"Number of communities: {len(partition)}")
    for i, community in enumerate(partition):
        print(f"Community {i+1}: {community}")
    return leiden_communities
        
def evaluate_communities():
    graph_path = os.path.join("input_graphs", "SampleGraph2.gml")
    G = nx.read_gml(graph_path)
    
    lc = leiden_communities()
    lcm = nx.algorithms.community.modularity(G, lc)
    print("Leiden:", lcm)
    
def ARI(G, clustering, clustering_label="club"):
    """
    Computer the Adjust Rand Index (clustering accuracy) of "clustering" with "clustering_label" as ground truth.

    Parameters
    ----------
    G : NetworkX graph
        A given NetworkX graph with node attribute "clustering_label" as ground truth.
    clustering : dict or list or list of set
        Predicted community clustering.
    clustering_label : str
        Node attribute name for ground truth.

    Returns
    -------
    ari : float
        Adjust Rand Index for predicted community.
    """

    if util.find_spec("sklearn") is not None:
        from sklearn import preprocessing, metrics
    else:
        print("scikit-learn not installed, skipped...")
        return -1

    
    # Get the ground truth for the graph
    df = pd.read_csv("email-Eu-core-department-labels.txt")
    
    df[['0', '1']] = df['0 1'].str.split(' ', n=1, expand=True)
    df = df.drop('0 1', axis=1)
    df.loc[-1] = {'0': 0, '1': 1}  # adding a row
    df.index = df.index + 1  # shifting index
    df.sort_index(inplace=True) 
    df['0'] = df['0'].astype(int)
    df['1'] = df['1'].astype(int)
    
    num_communities = max(df['1'])
    groups = dict()
    for i in range(df['0'].size):
        groups.update({df['0'][i]: df['1'][i]})

    le = preprocessing.LabelEncoder()
    y_true = le.fit_transform(list(complex_list.values()))

    if isinstance(clustering, dict):
        # python-louvain partition format
        y_pred = np.array([clustering[v] for v in complex_list.keys()])
    elif isinstance(clustering[0], set):
        # networkx partition format
        predict_dict = {c: idx for idx, comp in enumerate(clustering) for c in comp}
        y_pred = np.array([predict_dict[v] for v in complex_list.keys()])
    elif isinstance(clustering, list):
        # sklearn partition format
        y_pred = clustering
    else:
        return -1

    return metrics.adjusted_rand_score(y_true, y_pred)