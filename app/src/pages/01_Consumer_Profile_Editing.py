import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout= 'wide')

API_BASE_URL = "http://web-api:4000"

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

"""
Purpose: to make the user have the ability to update profile information
i.e. only if their email changed
Because the UI is limited to only 1 user, the ability to change profile name is disabled.
"""

st.title("Edit Your Profile")
st.markdown("Use the form below to update your profile information.")

st.write('---')

# style button:
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #A78BFA;
        color: #1E293B;
        border-radius: 20 px;
        padding: 5px 15px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #9370DB;
        color: #E2E8F0;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

with st.form("edit_profile_form", 
             clear_on_submit=False, 
             enter_to_submit= False, 
             border=True, 
             width='stretch'):
    
    st.subheader("Account Details")

    # Values user can't edit:
    first_name_display = st.text_input("First Name", value=st.session_state.first_name, disabled=True)
    last_name_display = st.text_input("Last Name", value=st.session_state.last_name, disabled=True)

    # Value user can edit:
    new_email = st.text_input("Email Address", value=st.session_state.email)
    
    submitted = st.form_submit_button("✅ Apply Changes")

    if submitted:
        st.session_state.first_name = first_name_display
        st.session_state.last_name = last_name_display
        st.session_state.email = new_email

        st.success("Profile Details updated successfully!")
        st.success("Returning to profile page...")
        st.switch_page("pages/00_Consumer_Profile.py")

if st.button("Cancel & Go Back", key="canel_button"):
    st.switch_page("pages/00_Consumer_Profile.py")
