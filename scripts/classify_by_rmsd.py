import pandas as pd

features = pd.read_csv("data/annotations/rmsd_features.csv")

rmsd_cols = [c for c in features.columns if c.startswith("rmsd_to_")]

rows = []

for _, row in features.iterrows():
    best_col = row[rmsd_cols].idxmin()
    predicted_state = best_col.replace("rmsd_to_", "")

    rows.append({
        "pdb_id": row["pdb_id"],
        "predicted_state": predicted_state,
        "best_rmsd": row[best_col],
    })

out = pd.DataFrame(rows)
out.to_csv("data/annotations/rmsd_predictions.csv", index=False)

print(out)
