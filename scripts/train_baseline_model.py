import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

df = pd.read_csv("data/annotations/leut_feature_table.csv")

X = df.drop(columns=["pdb_id", "state"])
y = df["state"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

scores = cross_val_score(model, X, y, cv=3)

print("Cross-validation scores:", scores)
print("Mean accuracy:", scores.mean())

model.fit(X, y)

importances = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

print("\nFeature importances:")
print(importances)
