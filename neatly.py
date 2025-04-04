import datetime
import numpy as np
import pandas as pd
import random
import streamlit as st
# Add missing imports
import io
import base64
from PIL import Image
# Uncomment when you're ready to use pydicom
# import pydicom

# Initialize session state to track login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'active_page' not in st.session_state:
    st.session_state.active_page = "login"

# Function for health personnel login and registration 
def healthworker_login_form():
    """Function to enable logging in healthcare worker (2nd Access)"""
    access_records, sign_up = st.tabs(["Access Records", "Request Access"])

    with sign_up:
        with st.form(key="Sign_Up", clear_on_submit=True):
            st.subheader("Sign-Up")
            hw_username = st.text_input("Username")
            hw_email = st.text_input("Email")
            hw_password = st.text_input("Password", type="password")
            hw_unit = st.text_input("Unit (e.g: Dermatology)")
            hw_title = st.text_input("Title (e.g: Dr)")
            hw_rank = st.text_input("Rank (e.g: Snr. Resident/Matron)")
            hospital_name = st.text_input("Hospital Name")
            hospital_country = st.text_input("Country where hospital is located")
            hospital_province = st.text_input("Province/State/County/District Hospital is located")
            
            if st.form_submit_button("Create Account"):
                if not hw_username or not hw_email or not hw_password:
                    st.error("Please fill in all required fields.")
                # Uncomment when database is set up
                # elif credentials_collection.find_one({"$or": [{"Name": hw_username}, {"Email": hw_email}]}):
                #     st.error("Username or Email already exists.")
                else:
                    data = {
                        "Name": hw_username,
                        "Email": hw_email,
                        "Password": hw_password,
                        "Unit": hw_unit,
                        "Title": hw_title,
                        "Rank": hw_rank,
                        "Hospital": hospital_name,
                        "Country": hospital_country,
                        "Province": hospital_province
                    }
                    # Uncomment when database is set up
                    # credentials_collection.insert_one(data)
                    st.success("Account Created. Awaiting Approval From Hospital EHR Admin.")
    
    with access_records:
        with st.form(key="Healthworker_Form", clear_on_submit=False):
            st.subheader("Access Health Records")
            healthworker_username = st.text_input("Username")
            healthworker_password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Submit"):
                if not healthworker_username or not healthworker_password:
                    st.error("Enter Username & Password")
                else:
                    # For now using a simple authentication method (replace with database later)
                    # Uncomment and modify when database is set up
                    # hw_details = credentials_collection.find_one({
                    #     "Name": healthworker_username, "Password": healthworker_password
                    # })
                    
                    # For testing - Remove this when database is connected
                    hw_details = {"Name": healthworker_username} if healthworker_username == "test" and healthworker_password == "test" else None
                    
                    if not hw_details:
                        st.error("Invalid Username/Password")
                    else:
                        st.success("Access Granted")
                        st.session_state.logged_in = True
                        st.session_state.current_user = healthworker_username
                        st.session_state.active_page = "dashboard"
                        st.rerun()  # Force a rerun to update the UI

def add_new_patient_with_ocr():
    """Use OCR To Extract Details From Patient ID And Register Patient's Details In EHR System"""
    st.subheader("Register New Patient via ID Scan")
    enable_camera = st.checkbox("Enable Camera")
    scan_patient_id = st.camera_input("Scan Patient's ID To Fill Details", disabled=not enable_camera)
    if scan_patient_id:
        st.image(scan_patient_id)
        # Future OCR implementation will go here

def add_new_patient_typing():
    """Add Patient's Details By Typing"""
    st.subheader("Register New Patient")
    
    with st.form(key="patient_registration", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_id = st.text_input("Patient ID")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            dob = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        with col2:
            contact = st.text_input("Contact Number")
            email = st.text_input("Email Address")
            address = st.text_area("Address")
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            
        emergency_contact = st.text_input("Emergency Contact")
        medical_history = st.text_area("Brief Medical History")
        
        if st.form_submit_button("Register Patient"):
            # Logic to save patient data would go here
            # For now just show a success message
            st.success(f"Patient {first_name} {last_name} registered successfully!")
            return True
    
    return False

def patient_record():
    """Search and display patient records"""
    st.subheader("Patient Records")
    
    search_name = st.text_input("Search Patient by Name or ID")
    
    if search_name:
        # This would be replaced with actual database query
        # patient_data = patient_database.find_one({"Patient's Name": search_name})
        
        # For demo purposes
        st.success(f"Patient found: {search_name}")
        
        # Display patient basic info
        st.subheader("Patient Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Name:** John Doe")
            st.write("**ID:** 12345")
            st.write("**Age:** 45")
        with col2:
            st.write("**Gender:** Male")
            st.write("**Blood Type:** O+")
            st.write("**Contact:** 555-1234")
        
        # Clinical notes section
        st.subheader("Clinical Notes")
        
        # Take Clinic Notes By Typing
        clinic_notes_text = st.text_area("Clinical Notes (⌨️ Type)")
        
        # Take Clinic Notes By Audio
        clinic_notes_audio = st.audio_input("Clinical Notes (🎙️ Speak)")
        if clinic_notes_audio:
            st.audio(clinic_notes_audio)
            st.info("Audio transcription feature will be implemented soon")
        
        # Save notes button
        if st.button("Save Notes"):
            if clinic_notes_text:
                st.success("Clinical notes saved successfully")
        
        # Tabs for different sections
        medical_images, lab_investigation, other_details = st.tabs(["Medical Images", "Lab Investigation", "Other Details"])
        
        with medical_images:
            st.subheader("Medical Imaging Records")
            with st.expander("Upload & Display Medical Files"):
                uploaded_files = st.file_uploader("Upload Medical Files (Images, DICOM, PDFs, etc.)", accept_multiple_files=True)

                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        st.subheader(f"File: {uploaded_file.name}")
                        file_type = uploaded_file.type
                        file_bytes = uploaded_file.read()

                        # Image files
                        if file_type.startswith("image/"):
                            image = Image.open(io.BytesIO(file_bytes))
                            st.image(image, caption=uploaded_file.name, use_column_width=True)

                        # PDF files
                        elif file_type == "application/pdf":
                            base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
                            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
                            st.markdown(pdf_display, unsafe_allow_html=True)

                        # Text files
                        elif file_type.startswith("text/"):
                            content = file_bytes.decode("utf-8")
                            st.text_area("Text File Contents", content, height=300)
                        
                        # Video files
                        elif file_type.startswith("video/"):
                            st.video(io.BytesIO(file_bytes))

                        # DICOM files - uncomment when pydicom is imported
                        elif uploaded_file.name.lower().endswith(".dcm"):
                            st.warning("DICOM preview will be available soon")
                            # try:
                            #     dicom_data = pydicom.dcmread(io.BytesIO(file_bytes))
                            #     if 'PixelData' in dicom_data:
                            #         image = dicom_data.pixel_array
                            #         st.image(image, caption=f"DICOM: {uploaded_file.name}", use_column_width=True)
                            #     else:
                            #         st.warning("This DICOM file does not contain image data.")
                            #     # Show some metadata
                            #     st.json({elem.keyword: str(elem.value) for elem in dicom_data if elem.keyword})
                            # except Exception as e:
                            #     st.error(f"Failed to read DICOM file: {e}")

                        # Unknown/unsupported file types
                        else:
                            st.info(f"Cannot preview this file type directly: {file_type or uploaded_file.name.split('.')[-1]}")
                            st.download_button(label="Download File", data=file_bytes, file_name=uploaded_file.name)
        
        with lab_investigation:
            st.subheader("Laboratory Results")
            # Example lab data - replace with real data later
            lab_df = pd.DataFrame({
                "Test": ["Complete Blood Count", "Lipid Panel", "Liver Function", "Kidney Function", "Glucose"],
                "Result": ["Normal", "Elevated Cholesterol", "Normal", "Normal", "126 mg/dL"],
                "Reference Range": ["N/A", "<200 mg/dL", "N/A", "N/A", "70-99 mg/dL"],
                "Date": ["2023-01-15", "2023-01-15", "2023-01-15", "2023-01-15", "2023-01-15"]
            })
            st.table(lab_df)
            
            # Option to add new lab results
            st.subheader("Add New Lab Results")
            if st.button("Add Lab Results"):
                st.info("Lab results upload feature coming soon")
        
        with other_details:
            st.subheader("Insurance & Billing Information")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Insurance Provider:** HealthCare Plus")
                st.write("**Policy Number:** HCP-789456123")
                st.write("**Coverage Type:** Comprehensive")
            with col2:
                st.write("**Effective Date:** Jan 1, 2023")
                st.write("**Expiration Date:** Dec 31, 2023")
                st.write("**Co-Pay:** $25")

def physician_dashboard():
    """Main dashboard for physicians after login"""
    st.title(f"Welcome, Dr. {st.session_state.current_user}")
    
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Search Patient Records"):
            st.session_state.active_page = "patient_records"
            st.rerun()
    
    with col2:
        if st.button("👤 Register New Patient"):
            st.session_state.active_page = "add_patient"
            st.rerun()
    
    with col3:
        if st.button("📊 View Statistics"):
            st.session_state.active_page = "statistics"
            st.rerun()
    
    # Recent patients section (placeholder)
    st.subheader("Recent Patients")
    recent_patients = pd.DataFrame({
        "Patient ID": ["P001", "P002", "P003", "P004", "P005"],
        "Name": ["John Doe", "Jane Smith", "Robert Johnson", "Emily Williams", "Michael Brown"],
        "Last Visit": ["2023-04-01", "2023-04-02", "2023-04-02", "2023-04-03", "2023-04-03"],
        "Department": ["Cardiology", "Orthopedics", "Neurology", "Pediatrics", "General Medicine"]
    })
    st.dataframe(recent_patients)
    
    # Appointments for today (placeholder)
    st.subheader("Today's Appointments")
    appointments = pd.DataFrame({
        "Time": ["09:00", "10:30", "13:15", "14:45", "16:00"],
        "Patient": ["Sarah Connor", "John Smith", "Maria Garcia", "David Wilson", "Emma Thompson"],
        "Type": ["Follow-up", "New Patient", "Lab Review", "Follow-up", "Consultation"],
        "Status": ["Checked In", "Waiting", "Scheduled", "Scheduled", "Scheduled"]
    })
    st.dataframe(appointments)

def statistics_page():
    """Show hospital and patient statistics"""
    st.title("Hospital Statistics")
    
    # Create some demo metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Patients", "1,245", "+12")
    col2.metric("Inpatients", "87", "-3")
    col3.metric("Outpatients Today", "124", "+8")
    col4.metric("Avg. Wait Time", "32 min", "-5 min")
    
    # Create a demo chart
    st.subheader("Patient Admissions (Last 30 Days)")
    chart_data = pd.DataFrame(
        np.random.randn(30, 1).cumsum(axis=0) + 20,
        columns=['Admissions']
    )
    st.line_chart(chart_data)
    
    # Demo department statistics
    st.subheader("Department Statistics")
    dept_data = pd.DataFrame({
        "Department": ["Cardiology", "Orthopedics", "Neurology", "Pediatrics", "General Medicine", "Oncology"],
        "Patients": [125, 98, 76, 143, 210, 65],
        "Avg. Stay (days)": [4.2, 3.1, 5.7, 2.3, 1.8, 7.5],
        "Satisfaction": [4.5, 4.3, 4.7, 4.8, 4.2, 4.6]
    })
    st.dataframe(dept_data)
    
    if st.button("Back to Dashboard"):
        st.session_state.active_page = "dashboard"
        st.rerun()

def logout():
    """Log out the current user"""
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.active_page = "login"
    st.rerun()

# Main app logic
def main():
    st.set_page_config(page_title="Healthcare EHR System", layout="wide")
    
    # Display sidebar
    with st.sidebar:
        st.title("Healthcare EHR")
        
        if st.session_state.logged_in:
            st.write(f"Logged in as: **{st.session_state.current_user}**")
            
            if st.button("🏠 Dashboard"):
                st.session_state.active_page = "dashboard"
                st.rerun()
                
            if st.button("👤 Patient Records"):
                st.session_state.active_page = "patient_records"
                st.rerun()
                
            if st.button("➕ Register Patient"):
                st.session_state.active_page = "add_patient"
                st.rerun()
                
            if st.button("📊 Statistics"):
                st.session_state.active_page = "statistics"
                st.rerun()
                
            if st.button("🚪 Logout"):
                logout()
        else:
            st.write("Please log in to access the system")
    
    # Display main content based on active page
    if not st.session_state.logged_in:
        st.title("Healthcare Electronic Health Record System")
        healthworker_login_form()
    else:
        if st.session_state.active_page == "dashboard":
            physician_dashboard()
        elif st.session_state.active_page == "patient_records":
            patient_record()
        elif st.session_state.active_page == "add_patient":
            add_patient_tabs = st.tabs(["Manual Entry", "Scan ID"])
            with add_patient_tabs[0]:
                add_new_patient_typing()
            with add_patient_tabs[1]:
                add_new_patient_with_ocr()
        elif st.session_state.active_page == "statistics":
            statistics_page()

# Run the app
if __name__ == "__main__":
    main()
