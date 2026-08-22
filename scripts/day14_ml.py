import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.metrics import accuracy_score, roc_auc_score, balanced_accuracy_score

X = pd.read_csv("data/processed/ml_feature_matrix_X.csv", index_col=0)
y = pd.read_csv("data/processed/ml_feature_matrix_y.csv", index_col=0).iloc[:, 0]

models = {
    "logreg": Pipeline([("scale", StandardScaler()),
                         ("clf", LogisticRegression(penalty="l2", C=1.0, class_weight="balanced", max_iter=2000))]),
    "rf": Pipeline([("clf", RandomForestClassifier(n_estimators=300, max_depth=4, min_samples_leaf=2,
                                                    class_weight="balanced", random_state=0))]),
    "mlp": Pipeline([("scale", StandardScaler()),
                      ("clf", MLPClassifier(hidden_layer_sizes=(8,), alpha=1.0, early_stopping=True,
                                             max_iter=2000, random_state=0))]),
}

loo = LeaveOneOut()
results = {}
for name, pipe in models.items():
    y_pred = cross_val_predict(pipe, X, y, cv=loo, method="predict")
    y_proba = cross_val_predict(pipe, X, y, cv=loo, method="predict_proba")[:, 1]
    results[name] = {"accuracy": accuracy_score(y, y_pred),
                      "balanced_accuracy": balanced_accuracy_score(y, y_pred),
                      "roc_auc": roc_auc_score(y, y_proba)}
    print(name, results[name])

import os
os.makedirs("results/ml", exist_ok=True)
pd.DataFrame(results).T.to_csv("results/ml/loocv_performance.csv")