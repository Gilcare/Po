def add_new_patient_typing():
    """Add Patient's Details By Typing"""
    st.subheader("Add Patient Details By Typing")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", 0, 120)
    sex = st.selectbox("Sex", ["Male", "Female"])
    address = st.text_area("Address")
    email = st.text_input("Email")
    phone = st.text_input("phone number")
    origin = st.text_input("State & LGA/County")
    occupation = st.text_input("Occupation")
    religion = st.text_input("Religion")
    hle = st.text_input("Highest Level of Education")

    clinic_notes_text = st.text_area("Clinical Notes(⌨️ Type)")
    clinic_notes_audio = st.audio_input("Clinical Notes(🎙️ Speak)")
    if clinic_notes_audio:
        st.audio(clinic_notes_audio)
        # Convert to text - Placeholder
        st.write("Audio transcription feature not implemented.")

    add_lab_investigations, add_medical_images, add_other_details = st.tabs(["Lab Investigation", "Medical Imaging", "Other Details"])
    with add_lab_investigations:
        st.write("Add logic for auto fill in with AI")

    with add_medical_images:
        # Logic for adding medical images
        with st.expander("Upload & Display Medical Files"):
            uploaded_files = st.file_uploader("Upload Medical Files (Images, DICOM, PDFs, etc.)", accept_multiple_files=True)

            if uploaded_files:
                for uploaded_file in uploaded_files:
                    st.subheader(f"File: {uploaded_file.name}")
                    file_type = uploaded_file.type
                    file_bytes = uploaded_file.read()
                    file_record = {
                        "fileName": uploaded_file.name,
                        "fileType": file_type,
                        "fileContent": file_bytes,  # store as binary or handle saving elsewhere
                            }

                    if file_type.startswith("image/"):
                        image = Image.open(io.BytesIO(file_bytes))
                        st.image(image, caption=uploaded_file.name, use_container_width=True)

                    elif file_type == "application/pdf":
                        base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)

                    elif file_type.startswith("text/"):
                        content = file_bytes.decode("utf-8")
                        st.text_area("Text File Contents", content, height=300)

                    elif file_type.startswith("video/"):
                        st.video(io.BytesIO(file_bytes))

                    elif uploaded_file.name.lower().endswith(".dcm"):
                        try:
                            dicom_data = pydicom.dcmread(io.BytesIO(file_bytes))
                            if 'PixelData' in dicom_data:
                                image = dicom_data.pixel_array
                                st.image(image, caption=f"DICOM: {uploaded_file.name}", use_column_width=True)
                            else:
                                st.warning("This DICOM file does not contain image data.")
                            st.json({elem.keyword: str(elem.value) for elem in dicom_data if elem.keyword})
                        except Exception as e:
                            st.error(f"Failed to read DICOM file: {e}")

                    else:
                        st.info(f"Cannot preview this file type directly: {file_type or uploaded_file.name.split('.')[-1]}")
                        st.download_button(label="Download File", data=file_bytes, file_name=uploaded_file.name)
                            
                    with st.expander("Physician's Summary Note About Above Image"):
                        st.text_input("Diagnosis, Differentials and Important Findings")
                        
                    

                    with st.expander("Physician's Summary Note About Above Image"):
                        diagnosis = st.text_area("Diagnosis")
                        differentials = st.text_area("Differential Diagnosis")
                        summary = st.text_area("Important Findings")
                        file_record["physicianNote"] = {
                            "diagnosis": diagnosis,
                            "differentials": differentials,
                            "summary": summary
                        }

                    medical_images_data.append(file_record)



    
    if st.button("Register Patient Details"):
        unique_id = str(uuid.uuid4())
        patient_data = {
           "patientID": unique_id,
           "personalDetails": {
                 "name": name,
                 "age": age,
                 "sex": sex,
                 "address": address,
                 "email": email,
                 "phone": phone,
                 "origin": origin,
                 "occupation": occupation,
                 "religion": religion,
                 "education": hle
                 },
           "clinicalNotes": {
               "text": clinic_notes_text,
               "audio": None}, # Handle audio transcription later
           "labInvestigations": [],  # You can append to this dynamically later
           "medicalImages": medical_images_data,  # File metadata here
            
            }

    result = patient_collection.insert_one(patient_data)
    st.success(f"Patient details saved with ID: {result.inserted_id}")















import uuid

def add_new_patient_typing():
    """Add Patient's Details By Typing"""
    st.subheader("Add Patient Details By Typing")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", 0, 120)
    sex = st.selectbox("Sex", ["Male", "Female"])
    address = st.text_area("Address")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    origin = st.text_input("State & LGA/County")
    occupation = st.text_input("Occupation")
    religion = st.text_input("Religion")
    hle = st.text_input("Highest Level of Education")

    clinic_notes_text = st.text_area("Clinical Notes (⌨️ Type)")
    clinic_notes_audio = st.audio_input("Clinical Notes (🎙️ Speak)")
    if clinic_notes_audio:
        st.audio(clinic_notes_audio)
        # Convert to text - Placeholder
        st.write("Audio transcription feature not implemented.")

    # Data holders
    lab_results = []
    medical_images_data = []

    add_lab_investigations, add_medical_images, add_other_details = st.tabs(["Lab Investigation", "Medical Imaging", "Other Details"])
    
    with add_lab_investigations:
        st.markdown("**Quick Fill Lab Results**")
        lab_test = st.selectbox("Select Common Lab Test", ["Complete Blood Count", "Malaria Parasite", "COVID-19 PCR", "Other"])
        lab_result = st.text_area("Result")
        if st.button("Add Lab Result"):
            lab_results.append({"test": lab_test, "result": lab_result})
            st.success("Lab result added")

    with add_medical_images:
        with st.expander("Upload & Display Medical Files"):
            uploaded_files = st.file_uploader("Upload Medical Files (Images, DICOM, PDFs, etc.)", accept_multiple_files=True)

            if uploaded_files:
                for uploaded_file in uploaded_files:
                    st.subheader(f"File: {uploaded_file.name}")
                    file_type = uploaded_file.type
                    file_bytes = uploaded_file.read()
                    file_record = {
                        "fileName": uploaded_file.name,
                        "fileType": file_type,
                        "fileContent": file_bytes,  # store as binary or handle saving elsewhere
                    }

                    if file_type.startswith("image/"):
                        image = Image.open(io.BytesIO(file_bytes))
                        st.image(image, caption=uploaded_file.name, use_container_width=True)

                    elif file_type == "application/pdf":
                        base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)

                    elif file_type.startswith("text/"):
                        content = file_bytes.decode("utf-8")
                        st.text_area("Text File Contents", content, height=300)

                    elif file_type.startswith("video/"):
                        st.video(io.BytesIO(file_bytes))

                    elif uploaded_file.name.lower().endswith(".dcm"):
                        try:
                            dicom_data = pydicom.dcmread(io.BytesIO(file_bytes))
                            if 'PixelData' in dicom_data:
                                image = dicom_data.pixel_array
                                st.image(image, caption=f"DICOM: {uploaded_file.name}", use_column_width=True)
                            else:
                                st.warning("This DICOM file does not contain image data.")
                            st.json({elem.keyword: str(elem.value) for elem in dicom_data if elem.keyword})
                        except Exception as e:
                            st.error(f"Failed to read DICOM file: {e}")

                    else:
                        st.info(f"Cannot preview this file type directly: {file_type or uploaded_file.name.split('.')[-1]}")
                        st.download_button(label="Download File", data=file_bytes, file_name=uploaded_file.name)

                    with st.expander("Physician's Summary Note About Above Image"):
                        diagnosis = st.text_area("Diagnosis")
                        differentials = st.text_area("Differential Diagnosis")
                        summary = st.text_area("Important Findings")
                        file_record["physicianNote"] = {
                            "diagnosis": diagnosis,
                            "differentials": differentials,
                            "summary": summary
                        }

                    medical_images_data.append(file_record)

    if st.button("Register Patient Details"):
        unique_id = str(uuid.uuid4())
        patient_data = {
            "patientID": unique_id,
            "personalDetails": {
                "name": name,
                "age": age,
                "sex": sex,
                "address": address,
                "email": email,
                "phone": phone,
                "origin": origin,
                "occupation": occupation,
                "religion": religion,
                "education": hle
            },
            "clinicalNotes": {
                "text": clinic_notes_text,
                "audio": None  # You can handle audio transcription later
            },
            "labInvestigations": lab_results,
            "medicalImages": medical_images_data,
            "medicalRecords": []  # Placeholder for future use
        }

        result = patient_collection.insert_one(patient_data)
        st.success(f"Patient details saved with ID: {result.inserted_id}")
        
