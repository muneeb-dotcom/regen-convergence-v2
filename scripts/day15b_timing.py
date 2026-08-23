import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeaveOneOut, cross_val_predict

X = pd.read_csv("data/processed/ml_feature_matrix_X.csv", index_col=0)
y = pd.read_csv("data/processed/ml_feature_matrix_y.csv", index_col=0).iloc[:, 0]

clf = RandomForestClassifier(n_estimators=100, max_depth=4, min_samples_leaf=2,
                              class_weight="balanced", random_state=0, n_jobs=1)

start = time.time()
pred = cross_val_predict(clf, X, y, cv=LeaveOneOut())
print("One LOO run took:", time.time() - start, "seconds")