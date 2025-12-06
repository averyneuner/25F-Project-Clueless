import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout= 'wide')

API_BASE_URL = "http://localhost:8501/"

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# API Calls Functions: (need to get consumer information)
# TODO: need to write a backend query + route to get the consumer information fron db.

if 'customer_id' not in st.session_state:
    st.session_state['customer_id'] = 13
    st.session_state['first_name'] = 'Rachel'
    st.session_state['last_name'] = 'Green'
    st.session_state['email'] = 'rachel.green@example.com'
    st.session_state['closet_size'] = 45 # place holder number
    st.session_state['outfits_count'] = 13 # place holder number

st.title(f"{st.session_state['first_name']}'s Profile")
st.markdown("Manage your account settings and view your closet statistics.")

st.write('---')

col1, col2 = st.columns([1, 2])


# optional profile picture:
with col1:
    st.subheader("Profile Picture")
    st.image("assets/profile_pic_placeholder.png", width=150)
    st.write(f"User ID: {st.session_state.user_id}")

# account details + closet stats:
with col2:
    st.subheader("Account Details")
    st.markdown(f"**Name:** {st.session_state.first_name} {st.session_state.last_name}")
    st.markdown(f"**Email:** {st.session_state.email}")

    st.subheader("Closet Statistics")
    st.progress(st.session_state.closet_size / 100, text=f"{st.session_state.closet_size} items in closet (100 max)")
    st.markdown(f"**Outfits Generated:** {st.session_state.outfits_count}")

st.write("---")

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

if st.button(f"✏️ Edit Profile Information", key="edit_profile_button"):
    st.switch_page("pages/01_Consumer_Profile_Editing.py")