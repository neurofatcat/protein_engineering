import streamlit as st
import py3Dmol
import os

# App Title
st.title("Protein Engineering App")

# Upload a PDB File
st.write("Upload a PDB file to visualize its structure:")
uploaded_file = st.file_uploader("Choose a PDB file", type=["pdb"])

# Function to visualize the PDB file
def visualize_pdb(pdb_string):
    """Render a 3D molecular structure using py3Dmol."""
    view = py3Dmol.view(width=800, height=400)
    view.addModel(pdb_string, "pdb")  # Add the model
    view.setStyle({"cartoon": {"color": "spectrum"}})  # Cartoon style with spectrum coloring
    view.zoomTo()  # Zoom to fit the structure
    return view

# Handle uploaded file
if uploaded_file:
    # Save the uploaded file temporarily
    temp_file_path = os.path.join("temp.pdb")
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Read the PDB file content
    with open(temp_file_path, "r") as pdb_file:
        pdb_content = pdb_file.read()
    
    # Display uploaded file name and size
    st.success(f"Uploaded: {uploaded_file.name}")
    st.write(f"File size: {len(uploaded_file.getbuffer()) / 1024:.2f} KB")
    
    # Visualize the PDB structure
    st.subheader("Protein Structure Visualization")
    structure_view = visualize_pdb(pdb_content)
    structure_html = structure_view.render()
    st.components.v1.html(structure_html, height=500)

    # Clean up temporary file
    os.remove(temp_file_path)
else:
    st.info("Please upload a PDB file to visualize its structure.")
