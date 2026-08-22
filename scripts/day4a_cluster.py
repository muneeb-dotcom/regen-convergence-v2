import scanpy as sc

adata = sc.read_h5ad("data/raw/GSE186527/adata_qc_final.h5ad")

adata_hvg = adata[:, adata.var.highly_variable].copy()
sc.pp.scale(adata_hvg, max_value=10)
sc.tl.pca(adata_hvg, n_comps=30, svd_solver="arpack")
sc.pp.neighbors(adata_hvg, n_neighbors=15)
sc.tl.leiden(adata_hvg, resolution=1.0)
sc.tl.rank_genes_groups(adata_hvg, "leiden", method="wilcoxon")

print(adata_hvg.obs["leiden"].value_counts())
print()
for cl in adata_hvg.obs["leiden"].cat.categories:
    top_genes = [adata_hvg.uns["rank_genes_groups"]["names"][cl][i] for i in range(10)]
    print(f"Cluster {cl}: {top_genes}")

adata_hvg.write("data/raw/GSE186527/adata_clustered.h5ad")