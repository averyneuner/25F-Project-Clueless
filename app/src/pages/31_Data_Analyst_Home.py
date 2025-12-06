import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

API_BASE_URL=""

# Show sidebar links for the role of the user
SideBarLinks()

# Initialize the session state:
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = 'Guest'
if 'active_category' not in st.session_state:
    st.session_state.active_category = None

if 'active occasion' not in st.session_state:
    st.session_state.active_occasion = None

st.title("Analytics")
st.write('')
st.write('')

# Layout
col1,col2 = st.columns(2)

# Overall Aesthetics and Trend Projection
with col1:
    st.subheader("Overall Aesthetics")
    st.write("◐")
    st.write("Vintage")
    
    st.write('')
    st.subheader("Trend Projection")
    st.write("📊 Monthly trend data visualization")


# Pieces by Wearability
with col2:
    st.subheader("Pieces by Wearability")
    
    pieces = [
        {"id": 1, "icon": "👕", "name": "Classic White Blouse"},
        {"id": 2, "icon": "👕", "name": "Graphic T-Shirts"},
        {"id": 3, "icon": "👕", "name": "Maxi Skirts"},
        {"id": 4, "icon": "👕", "name": "Cardigans"}
    ]
    
    for piece in pieces:
        if st.button(f"{piece['icon']}  {piece['name']}", key=f"piece_{piece['id']}", use_container_width=True):
            st.toast(f"Viewing {piece['name']}", icon='👀')