import pandas as pd

df = pd.read_csv("data/annotations/rmsd_evaluation.csv")

failures = df[df["correct"] == False]

print(failures[["pdb_id", "state", "predicted_state", "notes"]])

failures.to_csv("data/annotations/rmsd_failures.csv", index=False)
