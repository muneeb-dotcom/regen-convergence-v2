import pandas as pd

D3_specific = pd.read_csv("results/de_tables/digit_regeneration_specific_genes.csv")["0"].tolist()

skin = pd.read_csv("data/processed/skin_pseudobulk_counts.csv", index_col=0)
p3 = pd.read_csv("data/processed/digit_P3_counts.csv", index_col=0)
p2 = pd.read_csv("data/processed/digit_P2_counts.csv", index_col=0)

present_all = [g for g in D3_specific if g in skin.index and g in p3.index and g in p2.index]
print("Genes in all 3 datasets:", len(present_all))

pd.Series(present_all, name="gene").to_csv("results/de_tables/expanded_gene_set.csv", index=False)