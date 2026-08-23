import os
os.environ["LOKY_MAX_CPU_COUNT"] = "1"

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.metrics import accuracy_score
from sklearn.base import clone

X = pd.read_csv("data/processed/ml_feature_matrix_X_expanded.csv", index_col=0)
y = pd.read_csv("data/processed/ml_feature_matrix_y_expanded.csv", index_col=0).iloc[:, 0]

pipe = Pipeline([("clf", RandomForestClassifier(n_estimators=100, max_depth=4, min_samples_leaf=2,
                                                 class_weight="balanced", random_state=0, n_jobs=1))])

loo = LeaveOneOut()
observed = cross_val_predict(pipe, X, y, cv=loo, method="predict")
observed_acc = accuracy_score(y, observed)
print("Observed accuracy:", observed_acc)

rng = np.random.default_rng(0)
n_perm = 50
null_accs = []
for i in range(n_perm):
    y_shuffled = rng.permutation(y.values)
    pred = cross_val_predict(clone(pipe), X, y_shuffled, cv=loo, method="predict")
    null_accs.append(accuracy_score(y_shuffled, pred))
    print("perm", i+1, "done")

p_value = (np.sum(np.array(null_accs) >= observed_acc) + 1) / (n_perm + 1)
print("P-value:", p_value)

pd.DataFrame({"observed_acc":[observed_acc], "p_value":[p_value]}).to_csv("results/ml/permutation_test_expanded.csv", index=False)