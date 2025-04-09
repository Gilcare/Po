import streamlit as st
import pandas as pd
import uuid
from PIL import Image
import io
import base64
import pydicom

# Initialize session state
if 'lab_results' not in st.session_state:
    st.session_state.lab_results = []
if 'medical_images_data' not in st.session_state:
    st.session_state.medical_images_data = []

def get_lab_results():
    if st.session_state.lab_results:
        lab_df = pd.DataFrame(st.session_state.lab_results)
        return lab_df
    return pd.DataFrame(columns=["Test Name", "Result"])

def add_lab_result(test_name, result):
    st.session_state.lab_results.append({"Test Name": test_name, "Result": result})

def display_lab_results():
    st.subheader("Lab Results")
    lab_df = get_lab_results()
    edited_df = st.data_editor(lab_df, column_config={
        "Test Name": st.column_config.SelectboxColumn("Select Test", options=["Complete Blood Count", "Malaria Parasite", "COVID-19 PCR", "Other"]),
        "Result": st.column_config.TextColumn("Enter Result")
    }, use_container_width=True, num_rows="dynamic")
    if st.button("Add Lab Results"):
        st.session_state.lab_results = edited_df.to_dict('records')
        st.success("Lab results added successfully!")

def display_medical_images():
    # Logic for adding medical images
    with st.expander("Upload & Display Medical Files"):
        uploaded_files = st.file_uploader("Upload Medical Files (Images, DICOM, PDFs, etc.)", accept_multiple_files=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                st.subheader(f"File: {uploaded_file.name}")
                file_type = uploaded_file.type
                
                # Reset position to beginning of file
                uploaded_file.seek(0)
                file_bytes = uploaded_file.read()
                
                # Display file content based on file type
                if file_type.startswith('image/'):
                    st.image(file_bytes, caption=uploaded_file.name)
                elif '.dcm' in uploaded_file.name.lower():
                    try:
                        # Create a BytesIO object from file_bytes
                        bytes_io = io.BytesIO(file_bytes)
                        # Read DICOM file
                        ds = pydicom.dcmread(bytes_io)
                        st.write(f"DICOM file: {ds}")
                        # Add more DICOM-specific display logic here
                    except Exception as e:
                        st.error(f"Error processing DICOM file: {e}")
                else:
                    st.write("File format not supported for preview")
                
                # Save to session state
                file_id = str(uuid.uuid4())
                st.session_state.medical_images_data.append({
                    "id": file_id,
                    "name": uploaded_file.name,
                    "type": file_type,
                    "data": base64.b64encode(file_bytes).decode()
                })

def main():
    st.title("Patient Details")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", 0, 120)
    sex = st.selectbox("Sex", ["Male", "Female"])

    add_lab_investigations, add_medical_images = st.tabs(["Lab Investigation", "Medical Imaging"])

    with add_lab_investigations:
        display_lab_results()

    with add_medical_images:
        display_medical_images()

    if st.button("Register Patient Details"):
        if name and age > 0:
            # Save patient details (this would connect to a database in a real application)
            st.success("Patient details saved successfully!")
        else:
            st.error("Please fill in required patient information")

if __name__ == "__main__":
    main()
