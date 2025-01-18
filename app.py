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
    return view.js()  # Return the JavaScript code for rendering

# Handle uploaded file
if uploaded_file:
    # Read the PDB file content
    pdb_content = uploaded_file.getvalue().decode("utf-8")
    
    # Display uploaded file name and size
    st.success(f"Uploaded: {uploaded_file.name}")
    st.write(f"File size: {len(uploaded_file.getbuffer()) / 1024:.2f} KB")
    
    # Visualize the PDB structure
    st.subheader("Protein Structure Visualization")
    visualization_js = generate_3d_visualization(pdb_content)
    
    # Embed the visualization in Streamlit using HTML
    st.components.v1.html(f"""
    <div id="3dmolviewer" style="width: 800px; height: 400px;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.0.3/3Dmol-min.js"></script>
    <script>
    var viewer = $3Dmol.createViewer("3dmolviewer", {{ defaultcolors: $3Dmol.rasmolElementColors }});
    {visualization_js}
    </script>
    """, height=450)
else:
    st.info("Please upload a PDB file to visualize its structure.")
