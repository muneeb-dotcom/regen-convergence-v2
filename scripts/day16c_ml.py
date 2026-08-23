import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.metrics import accuracy_score, roc_auc_score, balanced_accuracy_score

X = pd.read_csv("data/processed/ml_feature_matrix_X_expanded.csv", index_col=0)
y = pd.read_csv("data/processed/ml_feature_matrix_y_expanded.csv", index_col=0).iloc[:, 0]

pipe = Pipeline([("clf", RandomForestClassifier(n_estimators=100, max_depth=4, min_samples_leaf=2,
                                                 class_weight="balanced", random_state=0, n_jobs=1))])

loo = LeaveOneOut()
y_pred = cross_val_predict(pipe, X, y, cv=loo, method="predict")
y_proba = cross_val_predict(pipe, X, y, cv=loo, method="predict_proba")[:, 1]

print("accuracy:", accuracy_score(y, y_pred))
print("balanced_accuracy:", balanced_accuracy_score(y, y_pred))
print("roc_auc:", roc_auc_score(y, y_proba))

pd.DataFrame({"accuracy":[accuracy_score(y, y_pred)],
              "balanced_accuracy":[balanced_accuracy_score(y, y_pred)],
              "roc_auc":[roc_auc_score(y, y_proba)]}).to_csv("results/ml/loocv_performance_expanded.csv", index=False)