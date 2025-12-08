import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout= 'wide')

API_BASE_URL = "http://localhost:4000/"

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

def get_customer_closets(customer_id):
    try:
        response = requests.get(f"{API_BASE_URL}/customer/{customer_id}/closets")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend at {API_BASE_URL}")
        return []
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ HTTP Error")
        return []
    except Exception as e:
        st.error(f"❌ error")
        return []
    

if 'customer_id' not in st.session_state:
    st.session_state['customer_id'] = 13
    st.session_state['first_name'] = 'Rachel'
    st.session_state['last_name'] = 'Green'
    st.session_state['email'] = 'rachel.green@example.com'

# Gets overall consumer closet data:
closets = get_customer_closets(st.session_state['customer_id'])

# For closet summary:
closet_size = sum(c.get('item_count', 0) for c in closets)
outfits_count = sum(c.get('outfit_count', 0) for c in closets)

st.title(f"{st.session_state['first_name']}'s Profile")
st.markdown("Manage your account settings and view your closet statistics.")

st.write('---')

col1, col2 = st.columns([1, 2])


# optional profile picture:
with col1:
    st.subheader("Profile Picture")
    st.image("assets/profile_pic_placeholder.png", width=150)
    st.write(f"Customer ID: {st.session_state.customer_id}")

# account details + closet stats:
with col2:
    st.subheader("Account Details")
    st.markdown(f"**Name:** {st.session_state.first_name} {st.session_state.last_name}")
    st.markdown(f"**Email:** {st.session_state.email}")

    st.subheader("Closet Statistics")
    st.progress(closet_size / 100, text=f"{closet_size} items in closet (100 max)")
    st.markdown(f"**Outfits Generated:** {outfits_count}")

st.write("---")

# style button:
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #A78BFA;
        color: #1E293B;
        border-radius: 20px;
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