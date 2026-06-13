from Bio.PDB import PDBParser

pdb_file = "data/structures/3TT1.pdb"

parser = PDBParser(QUIET=True)

structure = parser.get_structure("3TT1", pdb_file)

print("Chains:")
for chain in structure[0]:
    print(chain.id)

print("Atoms:", len(list(structure.get_atoms())))