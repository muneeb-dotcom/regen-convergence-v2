import pandas as pd

genes = pd.read_csv("results/de_tables/expanded_gene_set.csv")["gene"].tolist()

def load_and_zscore(counts_csv, meta_csv, genes, label_map, label_col):
    counts = pd.read_csv(counts_csv, index_col=0).T
    meta = pd.read_csv(meta_csv, index_col=0)
    present = [g for g in genes if g in counts.columns]
    counts = counts[present]
    z = (counts - counts.mean()) / counts.std(ddof=0)
    y = meta[label_col].map(label_map)
    return z, y

X_skin, y_skin = load_and_zscore(
    "data/processed/skin_pseudobulk_counts.csv",
    "data/processed/skin_sample_metadata.csv",
    genes, {"regenerative": 1, "scarring": 0, "baseline": None}, "condition"
)

X_p3, y_p3 = load_and_zscore(
    "data/processed/digit_P3_counts.csv",
    "data/processed/digit_P3_metadata.csv",
    genes, {t: 1 for t in ["0h","3h","6h","12h","24h","3d","7d","14d","21d"]}, "timepoint"
)

X_p2, y_p2 = load_and_zscore(
    "data/processed/digit_P2_counts.csv",
    "data/processed/digit_P2_metadata.csv",
    genes, {t: 0 for t in ["0h","3h","6h","12h","24h","3d","7d","14d","21d"]}, "timepoint"
)

X = pd.concat([X_skin, X_p3, X_p2]).fillna(0)
y = pd.concat([y_skin, y_p3, y_p2])

mask = y.notna()
X = X[mask]
y = y[mask]

print("Shape:", X.shape)
print(y.value_counts())

X.to_csv("data/processed/ml_feature_matrix_X_expanded.csv")
y.to_csv("data/processed/ml_feature_matrix_y_expanded.csv")