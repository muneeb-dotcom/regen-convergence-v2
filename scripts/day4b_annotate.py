import scanpy as sc
import pandas as pd

full = sc.read_h5ad("data/raw/GSE186527/adata_qc_final.h5ad")
clustered = sc.read_h5ad("data/raw/GSE186527/adata_clustered.h5ad")

fibroblast_clusters = ["0","1","3","4","6","8","13","15","16","17","18","19","21"]
cluster_to_type = {c: ("Fibroblast" if c in fibroblast_clusters else "Other") for c in clustered.obs["leiden"].cat.categories}
clustered.obs["cell_type"] = clustered.obs["leiden"].map(cluster_to_type)

full.obs["cell_type"] = clustered.obs["cell_type"].reindex(full.obs_names)

print(full.obs["cell_type"].value_counts())

fibro = full[full.obs["cell_type"] == "Fibroblast"]

counts = fibro.layers["counts"]
counts = counts.toarray() if hasattr(counts, "toarray") else counts

pseudobulk = (
    pd.DataFrame(counts, columns=fibro.var_names, index=fibro.obs_names)
    .groupby(fibro.obs["sample"].values)
    .sum()
    .T
)

pseudobulk = pseudobulk.round().astype(int)
pseudobulk.to_csv("data/processed/skin_pseudobulk_counts.csv")
print(pseudobulk.shape)
print(pseudobulk.head())