import networkx as nx
import os

def cut(graph, weight="weight"):
    G = graph
    max_weight = 0
    for (u, v) in G.edges():
        if G[u][v][weight] > max_weight:
            max_weight = G[u][v][weight]
    min_weight = max_weight
    for (u, v) in G.edges():
        if G[u][v][weight] < min_weight:
            min_weight = G[u][v][weight]

    increment = (max_weight - min_weight) / 100.0
    
    max_mod = 0
    best_graph = G
    threshold = max_weight
    best_communities = list()
    community_dict = dict()
    for i in range(100):
        current_graph = G.copy()
        to_delete = list()
        for (u, v) in current_graph.edges():
            if current_graph[u][v][weight] >= threshold:
                to_delete.append((u, v))
                
        current_graph.remove_edges_from(to_delete)

        undirected = current_graph.copy().to_undirected()
        # connected_components returns a generator of sets; convert to a list so we can
        # both print all components and reuse it for modularity calculation
        communities = list(nx.connected_components(undirected))

        # Only compute modularity if G has edges and there is more than one community
        if G.number_of_edges() == 0 or current_graph.number_of_edges() == 0 or len(communities) <= 1:
            curr_mod = 0
        else:
            curr_mod = nx.algorithms.community.modularity(G, communities)
            
        if curr_mod > max_mod:
            best_communities = communities
            max_mod = curr_mod
            best_graph = current_graph.copy()
            
        threshold -= increment
        
        outdir = os.path.join(os.getcwd(), "output_graphs", G.graph.get('name', G.name if hasattr(G, 'name') else ''))
        outdir = os.path.join(outdir, "surgery")
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        nx.write_gexf(current_graph, os.path.join(outdir, "cut_%d.gexf" % i))
    
    # Print all connected components (as node lists)
    for idx, comp in enumerate(best_communities):
        community_dict.update({idx : comp})
        print(f"Component {idx}:", comp)
        
    best_outdir = os.path.join(os.getcwd(), "output_graphs", G.graph.get('name', G.name if hasattr(G, 'name') else ''))
    best_outdir = os.path.join(best_outdir, "surgery")
    nx.write_gexf(best_graph, os.path.join(best_outdir, "best_cut.gexf"))
    print("Modularities")
    print("Ricci Flow:", max_mod)
    return community_dict