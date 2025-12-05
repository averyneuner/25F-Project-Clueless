# TODO: add general items section and an outfits section

import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

API_BASE_URL = ""

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = 'BREAK123'

if 'first_name' not in st.session_state:
    st.session_state['first_name'] = "Rachel"

st.title(f"{st.session_state['first_name']}'s Closet")

st.write('---')

st.subheader("View Clothing Items or Outfits")

# style button:
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #A78BFA;
        color: #1E293B;
        border-radius: 20 px;
        padding: 10px 25px;
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

col1, col2 = st.columns([1, 2])
with col1:
    if st.button(f" My Clothing Items", key="all_clothing_items_button"):
        st.switch_page("pages/01_Consumer_Clothing_Items.py")

with col2:
    if st.button(f"My Outfits", key="all_outfits_button"):
        st.switch_page("pages/01_Consumer_Outfits.py")
