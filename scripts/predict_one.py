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

query_pdb = "3F3A"

query = df[df["pdb_id"] == query_pdb]
query_X = query.drop(columns=["pdb_id", "state"])

probs = model.predict_proba(query_X)[0]

print("Query:", query_pdb)

for state, prob in zip(model.classes_, probs):
    print(f"{state}: {prob:.3f}")

print("Prediction:", model.predict(query_X)[0])
