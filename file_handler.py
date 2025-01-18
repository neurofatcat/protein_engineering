import os
from Bio.PDB import PDBParser

def save_uploaded_file(uploaded_file, upload_dir="inputs"):
    """
    Save the uploaded PDB file to the specified directory.
    """
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def parse_pdb_file(pdb_path):
    """
    Parse the PDB file to extract basic metadata.
    """
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("uploaded_structure", pdb_path)
    return {
        "num_chains": len(structure[0]),
        "num_residues": sum(1 for _ in structure.get_residues()),
        "num_atoms": sum(1 for _ in structure.get_atoms()),
    }
