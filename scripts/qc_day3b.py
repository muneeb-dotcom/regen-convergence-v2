import scanpy as sc
import scrublet as scr

adata = sc.read_h5ad("data/raw/GSE186527/adata_qc_stage1.h5ad")

scrub = scr.Scrublet(adata.X)
doublet_scores, predicted_doublets = scrub.scrub_doublets()
adata = adata[~predicted_doublets, :].copy()

sc.pp.highly_variable_genes(adata, n_top_genes=2000, flavor="seurat_v3")

adata.layers["counts"] = adata.X.copy()
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
adata.raw = adata

print(adata)
print("Doublets removed:", predicted_doublets.sum())

adata.write("data/raw/GSE186527/adata_qc_final.h5ad")