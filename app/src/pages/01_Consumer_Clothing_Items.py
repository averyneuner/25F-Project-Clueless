import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout= 'wide')

# TODO: API Base integration
API_BASE_URL = ""

# TODO: button for editing closet items (what view should it be?)
    # TODO: form for editing --> leads to another page w form to add new clothing item

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

if 'clothing_item' not in st.session_state:
    st.session_state['item_id'] = 'BREAK123'
    st.session_state['first_name'] = 'Rachel'
    st.session_state['last_name'] = 'Green'
    st.session_state['email'] = 'rachel.green@example.com'
    st.session_state['closet_size'] = 45 # place holder number
    st.session_state['outfits_count'] = 13 # place holder number

st.title(f"{st.session_state['first_name']}'s Closet")
st.markdown("Manage your closet and update your clothing items.")

# All clothing items (button for each category)
