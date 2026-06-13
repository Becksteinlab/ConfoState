import os
import math
import pandas as pd
from Bio.PDB import PDBParser

STRUCTURE_DIR = "data/structures"
OUTFILE = "data/annotations/gate_features.csv"

# First simple LeuT gate-distance features
# Uses CA atoms so it works even if side-chain atoms vary.
RESIDUE_PAIRS = {
    "ec_gate_R30_D404": (30, 404),
    "substrate_region_Y108_F253": (108, 253),
    "intracellular_region_R5_D369": (5, 369),
}

def get_ca_coord(pdb_file, residue_id, chain_id="A"):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("structure", pdb_file)
    chain = structure[0][chain_id]

    for residue in chain:
        if residue.id[1] == residue_id and "CA" in residue:
            return residue["CA"].coord

    return None

def distance(a, b):
    return math.sqrt(((a - b) ** 2).sum())

rows = []

for filename in sorted(os.listdir(STRUCTURE_DIR)):
    if not filename.endswith(".pdb"):
        continue

    pdb_id = filename.replace(".pdb", "")
    pdb_file = os.path.join(STRUCTURE_DIR, filename)

    row = {"pdb_id": pdb_id}

    for feature_name, (res1, res2) in RESIDUE_PAIRS.items():
        coord1 = get_ca_coord(pdb_file, res1)
        coord2 = get_ca_coord(pdb_file, res2)

        if coord1 is None or coord2 is None:
            row[feature_name] = None
        else:
            row[feature_name] = distance(coord1, coord2)

    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(OUTFILE, index=False)

print(f"Saved gate features to {OUTFILE}")
print(df.head())
