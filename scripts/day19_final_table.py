import pandas as pd

genes = pd.read_csv("results/de_tables/convergent_genes.csv")["gene"].tolist()

skin = pd.read_csv("results/de_tables/skin_DE_ranked_all_genes.csv", index_col=0)
skin_stats = skin.loc[skin.index.isin(genes), ["log2FoldChange", "padj"]].reset_index()
skin_stats.columns = ["gene", "logFC_skin", "padj_skin"]

string_c = pd.read_csv("results/network/string_centrality_lowconf.csv")
ion_flags = pd.read_csv("results/network/ion_channel_flags.csv")
ion_flags = ion_flags.rename(columns={"query": "gene"})
shap_rank = pd.read_csv("results/ml/shap_gene_ranking.csv")
shap_rank.columns = ["gene", "mean_abs_SHAP"]
pubmed = pd.read_csv("results/literature/pubmed_counts.csv")
pubmed.columns = ["gene", "pubmed_count"]

tier_map = {
    "Nfatc1": "Known regulator",
    "Sfrp4": "Known regulator",
    "Saa3": "Studied elsewhere",
    "Dusp4": "Studied elsewhere",
}
tier_df = pd.DataFrame({"gene": list(tier_map.keys()), "literature_tier": list(tier_map.values())})

final = (
    pd.DataFrame({"gene": genes})
    .merge(skin_stats, on="gene", how="left")
    .merge(string_c, on="gene", how="left")
    .merge(ion_flags, on="gene", how="left")
    .merge(shap_rank, on="gene", how="left")
    .merge(pubmed, on="gene", how="left")
    .merge(tier_df, on="gene", how="left")
)

print(final)
final.to_csv("results/final_evidence_table.csv", index=False)