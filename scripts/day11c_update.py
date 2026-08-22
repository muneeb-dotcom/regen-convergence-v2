import pandas as pd, networkx as nx

convergent = pd.read_csv("results/de_tables/convergent_genes.csv")["gene"].tolist()

G = nx.Graph()
G.add_nodes_from(convergent)
G.add_edge("Sfrp4", "Nfatc1", weight=0.209)

centrality = pd.DataFrame({
    "gene": list(G.nodes()),
    "degree": [d for _, d in G.degree()],
    "betweenness": list(nx.betweenness_centrality(G, weight="weight").values()),
})
centrality.to_csv("results/network/string_centrality_lowconf.csv", index=False)
print(centrality)