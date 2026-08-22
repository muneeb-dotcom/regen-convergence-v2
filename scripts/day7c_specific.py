import pandas as pd

D3 = set(pd.read_csv("results/de_tables/digit_P3_regeneration_responsive_genes.csv")["x"])
D2 = set(pd.read_csv("results/de_tables/digit_P2_injury_responsive_genes.csv")["x"])

D3_specific = D3 - D2

print(f"D3 (P3/regenerating): {len(D3)} genes")
print(f"D2 (P2/non-regenerating): {len(D2)} genes")
print(f"D3_specific (regeneration-specific): {len(D3_specific)} genes")

pd.Series(sorted(D3_specific)).to_csv("results/de_tables/digit_regeneration_specific_genes.csv", index=False)