import streamlit as st




def main():
    #======== Access Buttons For Different Users=======
    st.markdown("<h1 style='text-align: center; color: white;'>CareGrid</h1>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<p style='text-align: center; font-size: small; color: white; '>Log In As: </p>", unsafe_allow_html=True)
    left, middle, right = st.columns(3, vertical_alignment = "bottom")
    left.button("User", use_container_width = True)
    middle.button("Health personnel", use_container_width = True)
    right.button("Admin", use_container_width = True)
    #st.divider()




    #===== App ======
    if not st.experimental_user.is_logged_in:
        st.login("auth0")
    else:
        st.write(f"Hello, {st.experimental_user.name}!")












if __name__ == "__main__":
    main()
