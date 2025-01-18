import streamlit as st

# Title
st.title("Protein Engineering App")

# File uploader
st.write("Upload a PDB file to get started:")
uploaded_file = st.file_uploader("Choose a PDB file", type=["pdb"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    # Placeholder for further processing
    st.write("File processing will go here.")
