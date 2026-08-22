import mygene, pandas as pd

mg = mygene.MyGeneInfo()
convergent = pd.read_csv("results/de_tables/convergent_genes.csv")["gene"].tolist()
res = mg.querymany(convergent, scopes="symbol", species="mouse", fields="go.MF,go.CC", as_dataframe=True)

TARGET_GO = {"GO:0005216", "GO:0005243", "GO:0005921", "GO:0042625"}

def flag_gene(row):
    hits = set()
    for field in ("go.MF", "go.CC"):
        terms = row.get(field)
        if isinstance(terms, list):
            hits |= {t.get("id") for t in terms if isinstance(t, dict)}
        elif isinstance(terms, dict):
            hits.add(terms.get("id"))
    matched = hits & TARGET_GO
    return pd.Series({"ion_channel_flag": len(matched) > 0, "matched_GO_terms": ";".join(sorted(matched))})

flags = res.apply(flag_gene, axis=1)
print(flags)
flags.to_csv("results/network/ion_channel_flags.csv")