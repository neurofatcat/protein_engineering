import streamlit as st
import py3Dmol

# App Title
st.title("Protein Engineering App")

# Upload a PDB File
st.write("Upload a PDB file to visualize its structure:")
uploaded_file = st.file_uploader("Choose a PDB file", type=["pdb"])

# Function to generate the HTML for embedding py3Dmol
def generate_3d_visualization(pdb_string):
    """Generate HTML for 3D molecular visualization using py3Dmol."""
    view = py3Dmol.view(width=800, height=400)
    view.addModel(pdb_string, "pdb")  # Load PDB model
    view.setStyle({"cartoon": {"color": "spectrum"}})  # Cartoon style
    view.zoomTo()  # Fit to screen
    return view

# Handle uploaded file
if uploaded_file:
    # Read the PDB file content
    pdb_content = uploaded_file.getvalue().decode("utf-8")
    
    # Display uploaded file name and size
    st.success(f"Uploaded: {uploaded_file.name}")
    st.write(f"File size: {len(uploaded_file.getbuffer()) / 1024:.2f} KB")
    
    # Visualize the PDB structure
    st.subheader("Protein Structure Visualization")
    view = generate_3d_visualization(pdb_content)
    view_html = view._make_html()  # Generate HTML for embedding

    # Embed the HTML in Streamlit
    st.components.v1.html(view_html, height=450)
else:
    st.info("Please upload a PDB file to visualize its structure.")
