import pandas as pd

metadata = pd.read_csv("data/annotations/leut_metadata.csv")
preds = pd.read_csv("data/annotations/rmsd_predictions.csv")

df = metadata.merge(preds, on="pdb_id")

df = df.dropna(subset=["state"])
df = df[df["state"] != "unknown"]

df["correct"] = df["state"] == df["predicted_state"]

print(df[["pdb_id", "state", "predicted_state", "correct"]])

accuracy = df["correct"].mean()
print("\nAccuracy:", accuracy)

df.to_csv("data/annotations/rmsd_evaluation.csv", index=False)