import pandas as pd

metadata = pd.read_csv("data/annotations/leut_metadata.csv")
rmsd = pd.read_csv("data/annotations/rmsd_features.csv")
gates = pd.read_csv("data/annotations/gate_features.csv")

df = metadata[["pdb_id", "state"]].merge(rmsd, on="pdb_id").merge(gates, on="pdb_id")

df = df.dropna(subset=["state"])
df = df[df["state"] != "unknown"]

df.to_csv("data/annotations/leut_feature_table.csv", index=False)

print(df.head())
print("\nSaved to data/annotations/leut_feature_table.csv")
