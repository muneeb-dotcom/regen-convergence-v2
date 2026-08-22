import pandas as pd

p3 = pd.read_csv("data/processed/digit_P3_metadata.csv", index_col=0)
p2 = pd.read_csv("data/processed/digit_P2_metadata.csv", index_col=0)
print(p3["timepoint"].unique())
print(p2["timepoint"].unique())