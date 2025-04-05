with sign_up:
        with st.form(key="Sign_Up", clear_on_submit=True):
            st.subheader("Sign-Up")
            col1, col2 = st.columns(2)
            with col1:
              hw_firstname = st.text_input("Firstname*")
              hw_email = st.text_input("Email*")
              hw_password = st.text_input("Password*", type = "password", help = "Min 8 Characters alphanumeric, must contain special characters")
              hw_license_number = st.text_input("License Number*")

            with col2:
              hw_lastname = st.text_input("Lastname*")
              hw_username = st.text_input("Username*")
              hw_confirm_password = st.text_input("Confirm Password*", type="password")
              hw_title = st.selectbox("Title*", ["Dr.", "Prof.", "Nurse", "Other"])

            # Professional Information
            col3, col4 = st.columns(2)
            with col3:
              hw_specialty = st.selectbox("Medical Specialty*", ["General Practice", "Dermatology", "Cardiology", "Neurology", "Pediatrics", "Oncology", "Surgery", "Psychiatry", "OB/GYN", "Other"])
            with col4:
              hw_rank = st.selectbox("Rank*", ["Consultant", "Specialist", "Senior Resident", "Junior Resident", "Head Nurse", "Staff Nurse", "Other"])

            
            # Hospital Information - Added Address
            hospital_name = st.text_input("Hospital/Institution Name*")
            hospital_address = st.text_input("Hospital Address*")

            col5, col6 = st.columns(2)
            with col5:
              hospital_city = st.text_input("City*")
              hospital_country = st.selectbox("Country*", ["United States", "Canada", "United Kingdom", "Australia", "Nigeria", "Ghana", "South Africa", "Other"])
            with col6:
              hospital_province = st.text_input("Province/State*")
              hospital_department = st.text_input("Department/Unit*")

            # Verification - Simple Single Checkbox
            terms_checkbox = st.checkbox("I confirm that all information is accurate and I agree to the Terms of Service*")

            # Submit button
            submit_button = st.button("Register")
            
            if st.form_submit_button("Create Account"):
                if not hw_username or not hw_email or not hw_password:
                    st.error("Please fill in all required fields.")
                elif credentials_collection.find_one({"$or": [{"Name": hw_username}, {"Email": hw_email}]}):
                    st.error("Username or Email already exists.")
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
                    credentials_collection.insert_one(data)
                    st.success("Account Created. Awaiting Approval From Hospital





        # Updated Healthcare Professional Registration Form
col1, col2 = st.columns(2)

with col1:
    hw_firstname = st.text_input("First Name*")
    hw_email = st.text_input("Email Address*")
    hw_password = st.text_input("Password*", type="password", help="Min 8 characters")
    hw_license_number = st.text_input("License Number*")
    
with col2:
    hw_lastname = st.text_input("Last Name*")
    hw_username = st.text_input("Username*")
    hw_confirm_password = st.text_input("Confirm Password*", type="password")
    hw_title = st.selectbox("Title*", ["Dr.", "Prof.", "Nurse", "Other"])

# Professional Information - Added Rank
col3, col4 = st.columns(2)
with col3:
    hw_specialty = st.selectbox("Medical Specialty*", ["General Practice", "Dermatology", "Cardiology", "Neurology", "Pediatrics", "Oncology", "Surgery", "Psychiatry", "OB/GYN", "Other"])
with col4:
    hw_rank = st.selectbox("Rank*", ["Consultant", "Specialist", "Senior Resident", "Junior Resident", "Head Nurse", "Staff Nurse", "Other"])

# Hospital Information - Added Address
hospital_name = st.text_input("Hospital/Institution Name*")
hospital_address = st.text_input("Hospital Address*")

col5, col6 = st.columns(2)
with col5:
    hospital_city = st.text_input("City*")
    hospital_country = st.selectbox("Country*", ["United States", "Canada", "United Kingdom", "Australia", "Nigeria", "Ghana", "South Africa", "Other"])
with col6:
    hospital_province = st.text_input("Province/State*")
    hospital_department = st.text_input("Department/Unit*")

# Verification - Simple Single Checkbox
terms_checkbox = st.checkbox("I confirm that all information is accurate and I agree to the Terms of Service*")

# Submit button
submit_button = st.button("Register")

# Simple validation
if submit_button:
    # Hospital Information - Added Address
hospital_name = st.text_input("Hospital/Institution Name*")
hospital_address = st.text_input("Hospital Address*")

col5, col6 = st.columns(2)
with col5:
    hospital_city = st.text_input("City*")
    hospital_country = st.selectbox("Country*", ["United States", "Canada", "United Kingdom", "Australia", "Nigeria", "Ghana", "South Africa", "Other"])
with col6:
    hospital_province = st.text_input("Province/State*")
    hospital_department = st.text_input("Department/Unit*")

# Verification - Simple Single Checkbox
terms_checkbox = st.checkbox("I confirm that all information is accurate and I agree to the Terms of Service*")

# Submit button
submit_button = st.button("Register")
    else:
        st.success("Registration successful")
