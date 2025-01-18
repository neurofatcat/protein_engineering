import streamlit as st
import py3Dmol

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

# Display the visualized structure
def render_pdb_with_py3dmol(pdb_string):
    """Generate HTML to embed py3Dmol structure in Streamlit."""
    view = visualize_pdb(pdb_string)
    return view.show()

# Handle uploaded file
if uploaded_file:
    # Read the PDB file content
    pdb_content = uploaded_file.getvalue().decode("utf-8")
    
    # Display uploaded file name and size
    st.success(f"Uploaded: {uploaded_file.name}")
    st.write(f"File size: {len(uploaded_file.getbuffer()) / 1024:.2f} KB")
    
    # Visualize the PDB structure
    st.subheader("Protein Structure Visualization")
    render_pdb_with_py3dmol(pdb_content)
else:
    st.info("Please upload a PDB file to visualize its structure.")
