import scanpy as sc
import pandas as pd

sc.settings.verbosity = 2

samples = {
    "GSM5429653_T1": "baseline_unwounded",
    "GSM5429654_T2": "baseline_unwounded",
    "GSM5429655_T3": "baseline_unwounded",
    "GSM5429656_T-7P": "POD7_PBS",
    "GSM5429657_T-7V": "POD7_Verteporfin",
    "GSM5429658_T-14P": "POD14_PBS",
    "GSM5429659_T-14V": "POD14_Verteporfin",
    "GSM5429660_T-30P": "POD30_PBS",
    "GSM5429661_T-30V": "POD30_Verteporfin",
}

adatas = []
for prefix, condition in samples.items():
    a = sc.read_10x_mtx("data/raw/GSE186527/suppl_https/", prefix=prefix + "_")
    a.var_names_make_unique()
    a.obs["sample"] = prefix
    a.obs["condition"] = condition
    adatas.append(a)

adata = adatas[0].concatenate(adatas[1:], batch_key="sample_batch")

adata.var["mt"] = adata.var_names.str.startswith("mt-")
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True, percent_top=None)

adata = adata[adata.obs.n_genes_by_counts > 200, :]
adata = adata[adata.obs.n_genes_by_counts < 6000, :]
adata = adata[adata.obs.pct_counts_mt < 10, :]
sc.pp.filter_genes(adata, min_cells=3)

print(adata)
print(adata.obs["condition"].value_counts())

adata.write("data/raw/GSE186527/adata_qc_stage1.h5ad")

import scanpy as sc
import scrublet as scr

adata = sc.read_h5ad("data/raw/GSE186527/adata_qc_stage1.h5ad")

scrub = scr.Scrublet(adata.X)
doublet_scores, predicted_doublets = scrub.scrub_doublets()
adata = adata[~predicted_doublets, :].copy()

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
adata.raw = adata
sc.pp.highly_variable_genes(adata, n_top_genes=2000, flavor="seurat_v3")

print(adata)
print("Doublets removed:", predicted_doublets.sum())

adata.write("data/raw/GSE186527/adata_qc_final.h5ad")