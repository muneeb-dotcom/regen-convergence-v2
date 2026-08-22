import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# 1. Volcano plot — skin DE
skin = pd.read_csv("results/de_tables/skin_DE_ranked_all_genes.csv", index_col=0)
plt.figure(figsize=(6,5))
plt.scatter(skin["log2FoldChange"], -skin["padj"].apply(lambda x: 0 if pd.isna(x) else -1*__import__("math").log10(x) if x>0 else 0), s=5, alpha=0.4)
plt.xlabel("log2 Fold Change (Regenerative vs Scarring)")
plt.ylabel("-log10(padj)")
plt.title("Skin fibroblasts: Regenerative vs Scarring")
plt.axhline(-1*__import__("math").log10(0.05), color="red", linestyle="--", linewidth=0.8)
plt.tight_layout()
plt.savefig("results/figures/volcano_skin.png", dpi=150)
plt.close()

# 2. Bar chart — gene set sizes across days
sizes = {
    "Skin S\n(top 200)": 200,
    "Digit D3\n(regen)": 418,
    "Digit D2\n(non-regen)": 1909,
    "D3 specific\n(regen-only)": 170,
    "Convergent\n(skin ∩ digit)": 4,
}
plt.figure(figsize=(7,5))
plt.bar(sizes.keys(), sizes.values(), color="steelblue")
plt.ylabel("Number of genes")
plt.title("Gene set sizes across analysis stages")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("results/figures/geneset_sizes.png", dpi=150)
plt.close()

# 3. Venn diagram — convergent genes
D3_specific = set(pd.read_csv("results/de_tables/digit_regeneration_specific_genes.csv")["0"])
ranked = pd.read_csv("results/de_tables/skin_DE_ranked_all_genes.csv", index_col=0)
ranked["abs_stat"] = ranked["stat"].abs()
S = set(ranked.sort_values("abs_stat", ascending=False).head(200).index)

plt.figure(figsize=(5,5))
venn2([S, D3_specific], set_labels=("Skin (S)", "Digit regen-specific"))
plt.title("Gene-level convergence")
plt.tight_layout()
plt.savefig("results/figures/venn_convergence.png", dpi=150)
plt.close()

print("Saved 3 figures to results/figures/")