import requests, pandas as pd, networkx as nx

STRING_API = "https://string-db.org/api"
SPECIES = 10090

def get_string_ids(genes):
    params = {"identifiers": "\r".join(genes), "species": SPECIES, "limit": 1, "caller_identity": "regen_convergence_project"}
    r = requests.post(f"{STRING_API}/tsv/get_string_ids", data=params)
    return pd.read_csv(pd.io.common.StringIO(r.text), sep="\t")

def get_network(string_ids, score_threshold=150):
    params = {"identifiers": "\r".join(string_ids), "species": SPECIES,
              "required_score": score_threshold, "caller_identity": "regen_convergence_project"}
    r = requests.post(f"{STRING_API}/tsv/network", data=params)
    return pd.read_csv(pd.io.common.StringIO(r.text), sep="\t")

convergent = pd.read_csv("results/de_tables/convergent_genes.csv")["gene"].tolist()
id_map = get_string_ids(convergent)
edges = get_network(id_map["stringId"].tolist(), score_threshold=150)
print(edges)