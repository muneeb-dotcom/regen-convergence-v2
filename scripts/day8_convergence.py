import pandas as pd

ranked = pd.read_csv("results/de_tables/skin_DE_ranked_all_genes.csv", index_col=0)
ranked["abs_stat"] = ranked["stat"].abs()
S = set(ranked.sort_values("abs_stat", ascending=False).head(200).index)

D3_specific = set(pd.read_csv("results/de_tables/digit_regeneration_specific_genes.csv")["0"])

convergent = sorted(S & D3_specific)

print(f"S (skin, top 200 by |stat|): {len(S)} genes")
print(f"D3_specific (digit, regeneration-specific): {len(D3_specific)} genes")
print(f"Convergent: {len(convergent)} genes")
print(convergent)

pd.Series(convergent, name="gene").to_csv("results/de_tables/convergent_genes.csv", index=False)