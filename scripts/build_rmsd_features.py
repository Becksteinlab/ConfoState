import os
import pandas as pd
from Bio.PDB import PDBParser, Superimposer

STRUCTURE_DIR = "data/structures"
OUTFILE = "data/annotations/rmsd_features.csv"

REFERENCES = {
    "outward_open": "3TT1.pdb",
    "occluded": "3F3E.pdb",
    "inward_open": "3TT3.pdb",
    "inward_occluded": "6XWM.pdb",
    "outward_return": "5JAE.pdb",
}

def get_ca_atoms(pdb_file, chain_id="A"):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("structure", pdb_file)
    chain = structure[0][chain_id]

    atoms = []
    for residue in chain:
        if "CA" in residue:
            atoms.append(residue["CA"])
    return atoms

def calculate_rmsd(ref_file, mobile_file):
    ref_atoms = get_ca_atoms(ref_file)
    mobile_atoms = get_ca_atoms(mobile_file)

    n = min(len(ref_atoms), len(mobile_atoms))
    ref_atoms = ref_atoms[:n]
    mobile_atoms = mobile_atoms[:n]

    sup = Superimposer()
    sup.set_atoms(ref_atoms, mobile_atoms)

    return sup.rms

rows = []

for filename in sorted(os.listdir(STRUCTURE_DIR)):
    if not filename.endswith(".pdb"):
        continue

    pdb_id = filename.replace(".pdb", "")
    mobile_file = os.path.join(STRUCTURE_DIR, filename)

    row = {"pdb_id": pdb_id}

    for state, ref_name in REFERENCES.items():
        ref_file = os.path.join(STRUCTURE_DIR, ref_name)
        row[f"rmsd_to_{state}"] = calculate_rmsd(ref_file, mobile_file)

    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(OUTFILE, index=False)

print(f"Saved RMSD features to {OUTFILE}")
print(df.head())
