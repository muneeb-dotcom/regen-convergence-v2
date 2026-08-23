import pandas as pd
import shap
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

X = pd.read_csv("data/processed/ml_feature_matrix_X_expanded.csv", index_col=0)
y = pd.read_csv("data/processed/ml_feature_matrix_y_expanded.csv", index_col=0).iloc[:, 0]

clf = RandomForestClassifier(n_estimators=100, max_depth=4, min_samples_leaf=2,
                              class_weight="balanced", random_state=0, n_jobs=1)
clf.fit(X, y)

explainer = shap.TreeExplainer(clf)
shap_values = explainer.shap_values(X)

if isinstance(shap_values, list):
    sv = shap_values[1]
else:
    sv = shap_values[:, :, 1]

shap_df = pd.DataFrame(sv, columns=X.columns, index=X.index)
mean_abs_shap = shap_df.abs().mean().sort_values(ascending=False)
mean_abs_shap.to_csv("results/ml/shap_gene_ranking.csv")

print(mean_abs_shap.head(20))

shap.summary_plot(sv, X, show=False)
plt.savefig("results/figures/shap_summary.png", bbox_inches="tight")