from Bio.PDB import PDBParser, Superimposer

def get_ca_atoms(pdb_file, chain_id="A"):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("structure", pdb_file)
    chain = structure[0][chain_id]

    atoms = []
    for residue in chain:
        if "CA" in residue:
            atoms.append(residue["CA"])
    return atoms

ref_file = "data/structures/3TT1.pdb"
mobile_file = "data/structures/3F3A.pdb"

ref_atoms = get_ca_atoms(ref_file)
mobile_atoms = get_ca_atoms(mobile_file)

n = min(len(ref_atoms), len(mobile_atoms))
ref_atoms = ref_atoms[:n]
mobile_atoms = mobile_atoms[:n]

sup = Superimposer()
sup.set_atoms(ref_atoms, mobile_atoms)

print("RMSD:", sup.rms)
