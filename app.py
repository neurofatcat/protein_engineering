import streamlit as st
import py3Dmol
import pyrosetta

# Initialize PyRosetta
pyrosetta.init("-mute all")

# App Title
st.title("Protein Engineering App")

# Sidebar Navigation
st.sidebar.header("Navigation")
workflow = st.sidebar.radio(
    "Choose a module:",
    (
        "Upload and Visualize Protein",
        "Protein Preparation",
        "Ligand Preparation",
    ),
)

# Helper Function: Save file with custom name
def save_output_file(content, original_filename, module_name, extension="pdb"):
    """Save content to a file with a name including the original filename and module."""
    base_name = os.path.splitext(original_filename)[0]
    output_filename = f"{module_name}_{base_name}.{extension}"
    with open(output_filename, "w") as f:
        f.write(content)
    return output_filename

# Function to generate 3D visualization of PDB
def visualize_pdb(pdb_string):
    """Generate 3D visualization using py3Dmol."""
    view = py3Dmol.view(width=800, height=400)
    view.addModel(pdb_string, "pdb")  # Add the PDB model
    view.setStyle({"cartoon": {"color": "spectrum"}})  # Apply cartoon style
    view.zoomTo()  # Zoom to fit the model
    return view._make_html()

# Protein Preparation Logic
def prepare_protein(pdb_string):
    """Prepare protein: remove waters, add hydrogens, and optimize geometry."""
    pose = pyrosetta.pose_from_pdbstring(pdb_string)
    
    # Remove waters
    st.write("Removing water molecules...")
    waters_removed = pose.residues_from_subset(
        pyrosetta.rosetta.core.select.residue_selector.ResidueIndexSelector("HOH")
    )
    for i in sorted(waters_removed, reverse=True):
        pose.delete_residue_slow(i)
    
    # Add hydrogens
    st.write("Adding missing hydrogen atoms...")
    pyrosetta.rosetta.protocols.hydrogen_addition.AddHydrogenMover().apply(pose)
    
    # Optimize geometry
    st.write("Optimizing geometry (energy minimization)...")
    movemap = pyrosetta.MoveMap()
    movemap.set_bb(True)  # Allow backbone flexibility
    movemap.set_chi(True)  # Allow side-chain flexibility
    min_mover = pyrosetta.rosetta.protocols.minimization_packing.MinMover()
    min_mover.movemap = movemap
    min_mover.score_function(pyrosetta.get_fa_scorefxn())
    min_mover.apply(pose)
    
    # Return the modified PDB string
    return pose.dump_pdb()

# Main Area Logic
if workflow == "Upload and Visualize Protein":
    st.subheader("Upload and Visualize Protein")
    st.write("Upload a PDB file to visualize its structure:")
    uploaded_file = st.file_uploader("Choose a PDB file", type=["pdb"])
    
    if uploaded_file:
        # Read and display file
        pdb_content = uploaded_file.getvalue().decode("utf-8")
        st.success(f"Uploaded: {uploaded_file.name}")
        st.write(f"File size: {len(uploaded_file.getbuffer()) / 1024:.2f} KB")
        
        # Visualize PDB
        st.subheader("Protein Structure Visualization")
        structure_html = visualize_pdb(pdb_content)
        st.components.v1.html(structure_html, height=450)

elif workflow == "Protein Preparation":
    st.subheader("Protein Preparation")
    st.write("Prepare the uploaded protein for modeling workflows.")
    uploaded_file = st.file_uploader("Upload a PDB file for preparation", type=["pdb"])
    
    if uploaded_file:
        # Read and display file
        pdb_content = uploaded_file.getvalue().decode("utf-8")
        st.success(f"Uploaded: {uploaded_file.name}")
        
        # Call preparation function
        prepared_pdb = prepare_protein(pdb_content)
        
        # Save the prepared PDB
        prepared_filename = save_output_file(prepared_pdb, uploaded_file.name, "protein_prep", "pdb")
        st.success(f"Protein preparation complete. Saved as {prepared_filename}")
        st.download_button("Download Prepared Protein", prepared_pdb, file_name=prepared_filename)

elif workflow == "Ligand Preparation":
    st.subheader("Ligand Preparation")
    st.write("Prepare the uploaded ligand for docking or other workflows.")
    uploaded_file = st.file_uploader("Upload a ligand file (e.g., MOL2, SDF)", type=["mol2", "sdf"])
    
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        st.write("Ligand preparation steps would be applied here (placeholder).")

# Footer
st.markdown("---")
st.info("This app is a prototype for protein engineering workflows using Streamlit and PyRosetta.")
