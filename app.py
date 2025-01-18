import streamlit as st
from workflows.file_handler import save_uploaded_file, parse_pdb_file

# App Title
st.title("Levitate Bio Reverse Engineering: RFdiffusion App")

# File Upload
st.subheader("Step 1: Upload Target Protein")
uploaded_file = st.file_uploader("Upload a PDB file", type=["pdb"])

if uploaded_file:
    st.success(f"File uploaded: {uploaded_file.name}")

    # Save and parse file
    pdb_path = save_uploaded_file(uploaded_file)
    pdb_metadata = parse_pdb_file(pdb_path)

    # Display file metadata
    st.subheader("PDB File Metadata")
    st.write(f"Number of Chains: {pdb_metadata['num_chains']}")
    st.write(f"Number of Residues: {pdb_metadata['num_residues']}")
    st.write(f"Number of Atoms: {pdb_metadata['num_atoms']}")

    # Placeholder for the next step
    st.info("Next: Implement protein preparation workflows.")
