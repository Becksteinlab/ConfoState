import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/annotations/leut_feature_table.csv")

X = df.drop(columns=["pdb_id", "state"])
y = df["state"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X, y)

probs = model.predict_proba(X)
preds = model.predict(X)

rows = []

for i, pdb_id in enumerate(df["pdb_id"]):
    row = {
        "pdb_id": pdb_id,
        "true_state": y.iloc[i],
        "predicted_state": preds[i],
        "prediction_probability": probs[i].max(),
    }

    for state, prob in zip(model.classes_, probs[i]):
        row[f"prob_{state}"] = prob

    rows.append(row)

out = pd.DataFrame(rows)
out.to_csv("data/annotations/random_forest_predictions.csv", index=False)

print(out[["pdb_id", "true_state", "predicted_state", "prediction_probability"]])
print("\nSaved to data/annotations/random_forest_predictions.csv")
