import requests, pandas as pd, networkx as nx

STRING_API = "https://string-db.org/api"
SPECIES = 10090

def get_string_ids(genes):
    params = {"identifiers": "\r".join(genes), "species": SPECIES, "limit": 1, "caller_identity": "regen_convergence_project"}
    r = requests.post(f"{STRING_API}/tsv/get_string_ids", data=params)
    return pd.read_csv(pd.io.common.StringIO(r.text), sep="\t")

def get_network(string_ids, score_threshold=400):
    params = {"identifiers": "\r".join(string_ids), "species": SPECIES,
              "required_score": score_threshold, "caller_identity": "regen_convergence_project"}
    r = requests.post(f"{STRING_API}/tsv/network", data=params)
    return pd.read_csv(pd.io.common.StringIO(r.text), sep="\t")

convergent = pd.read_csv("results/de_tables/convergent_genes.csv")["gene"].tolist()
print("Genes:", convergent)

id_map = get_string_ids(convergent)
print(id_map)

edges = get_network(id_map["stringId"].tolist(), score_threshold=400)
print(edges)

G = nx.Graph()
G.add_nodes_from(convergent)
for _, row in edges.iterrows():
    G.add_edge(row["preferredName_A"], row["preferredName_B"], weight=row["score"])

centrality = pd.DataFrame({
    "gene": list(G.nodes()),
    "degree": [d for _, d in G.degree()],
    "betweenness": list(nx.betweenness_centrality(G, weight="weight").values()),
})

import os
os.makedirs("results/network", exist_ok=True)
centrality.to_csv("results/network/string_centrality.csv", index=False)
print(centrality)