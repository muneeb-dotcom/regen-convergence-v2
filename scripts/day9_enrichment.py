import pandas as pd
import gseapy as gp

ranked = pd.read_csv("results/de_tables/skin_DE_ranked_all_genes.csv", index_col=0)
ranked["abs_stat"] = ranked["stat"].abs()
S = list(ranked.sort_values("abs_stat", ascending=False).head(200).index)

D3_specific = list(pd.read_csv("results/de_tables/digit_regeneration_specific_genes.csv")["0"])

def run_enrichment(gene_list, label):
    enr = gp.enrichr(
        gene_list=gene_list,
        gene_sets=["GO_Biological_Process_2023", "KEGG_2019_Mouse", "Reactome_2022"],
        organism="mouse", outdir=f"results/enrichment/{label}", cutoff=0.05,
    )
    return enr.results

enr_S = run_enrichment(S, "skin")
enr_D3 = run_enrichment(D3_specific, "digit")

sig_S = set(enr_S.loc[enr_S["Adjusted P-value"] < 0.05, "Term"])
sig_D3 = set(enr_D3.loc[enr_D3["Adjusted P-value"] < 0.05, "Term"])
shared_terms = sig_S & sig_D3

print(f"Skin significant terms: {len(sig_S)}")
print(f"Digit significant terms: {len(sig_D3)}")
print(f"Shared terms: {len(shared_terms)}")
print(sorted(shared_terms))

pd.DataFrame({"Term": sorted(shared_terms)}).to_csv("results/enrichment/shared_pathway_terms.csv", index=False)