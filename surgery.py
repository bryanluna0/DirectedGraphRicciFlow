import networkx as nx
import os

def cut(graph):
    G = graph
    max_weight = 0
    for (u, v) in G.edges():
        if G[u][v]['weight'] > max_weight:
            max_weight = G[u][v]['weight']
    min_weight = max_weight
    for (u, v) in G.edges():
        if G[u][v]['weight'] < min_weight:
            min_weight = G[u][v]['weight']

    increment = (max_weight - min_weight) / 10.0
    
    max_mod = 0
    max_mod_i = 0
    best_graph = G
    threshold = max_weight
    for i in range(10):
        current_graph = G
        to_delete = list()
        for (u, v) in current_graph.edges():
            if current_graph[u][v]["weight"] >= threshold:
                to_delete.append((u, v))
                
        current_graph.remove_edges_from(to_delete)
                
        u_graph_connected = nx.connected_components(current_graph.to_undirected())
        curr_mod = nx.algorithms.community.modularity(current_graph, u_graph_connected)
        print(curr_mod)
        if (max_mod > curr_mod):
            max_mod = curr_mod
            max_mod_i = i
            best_graph = current_graph
        threshold -= increment
        if not os.path.isdir(os.path.join(os.getcwd(), "output_graphs", G.graph['name'], "surgery")):
            os.makedirs(os.path.join(os.getcwd(), "output_graphs", G.graph['name'], "surgery"))
        nx.write_gexf(best_graph, os.path.join("output_graphs", G.name, "surgery", "cut_%d.gexf"%i))
        
        
    nx.write_gexf(best_graph, os.path.join("output_graphs", G.name, "surgery", "best_cut.gexf"))
        