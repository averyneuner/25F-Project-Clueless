# TODO: add general items section and an outfits section

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

API_BASE_URL = "http://web-api:4000"

# API Functions:

# gets all closets for a given customer
def get_customer_closets(customer_id):
    try:
        response = requests.get(f"{API_BASE_URL}/customer/{customer_id}/closets")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend at {API_BASE_URL}")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ HTTP Error")
        return None
    except Exception as e:
        st.error(f"❌ error")
        return None

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

if 'customer_id' not in st.session_state:
    st.session_state['customer_id'] = 13
    st.session_state['first_name'] = 'Rachel'
    st.session_state['last_name'] = 'Green'
    st.session_state['email'] = 'rachel.green@example.com'

# user can select which closet to view:
if 'closet_id' not in st.session_state:
    st.session_state['closet_id'] = None

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

    .closet-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        background-color: #F9FAFB;
    }
    .closet-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 15px;
        font-size: 14px;
        font-weight: bold;
        background-color: #A78BFA;
        color: white;
        margin: 5px;
    }

    </style>
    """, 
    unsafe_allow_html=True
)

st.title(f"{st.session_state['first_name']}'s Closet")

st.subheader("View Clothing Items or Outfits")

st.divider()

closet_data = get_customer_closets(st.session_state['customer_id'])

if closet_data:
    items = closet_data.get('items', [])
    outfits = closet_data.get('outfits', [])

    closets = {}
    for item in items:
        closet_id = item['ClosetID']
        if closet_id not in closets:
            closets[closet_id] = {
                'id': closet_id,
                'items_count': 0,
                'outfits_count': 0
            }
        closets[closet_id]['items_count'] += 1

    for outfit in outfits:
        closet_id = outfit.get('ClosetID')
        if closet_id and closet_id in closets:
            closets[closet_id]['outfits_count'] += 1
    
    if not closets:
        st.info("You don't have any closets yet.")
    else:
        st.subheader("🗳️ Select a Closet")

        cols = st.columns(min(3, len(closets)))

        for idx, (closet_id, closet_info) in enumerate(closets.items()):
            with cols[idx % 3]:
                with st.container(border=True):
                    closet_names = {
                        109: "Gym Bag", 110: "Office Fits", 111: "Date Night",
                        112: "Casual", 113: "Summer 2025", 114: "Winter Vault",
                        115: "Interview Clothes", 116: "Lounge", 117: "Party Wear",
                        118: "Beach Trip", 119: "Hiking", 120: "Daily Rotation"
                    }
                    closet_name = closet_names.get(closet_id, f"Closet {closet_id}")

                    st.markdown(f"### 🗂️ {closet_name}")
                    st.markdown(
                        f'<span class="closet-badge">ID: {closet_id}</span>',
                        unsafe_allow_html=True
                    )

                    st.write()
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Items", closet_info['items_count'])
                    with col_b:
                        st.metric("Outfits", closet_info['outfits_count'])
                    
                    st.write("")
                    if st.button(f"Open Closet", key=f"open_closet_{closet_id}"):
                        st.session_state['closet_id'] = closet_id
                        st.session_state['closet_name'] = closet_name
                        st.rerun()

    st.divider()

    if st.session_state.get('closet_id'):
            current_closet_name = st.session_state.get('closet_name', f"Closet {st.session_state['closet_id']}")
            
            st.subheader(f"📂 Currently Viewing: {current_closet_name}")
            st.caption(f"Closet ID: {st.session_state['closet_id']}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("👗 View Clothing Items", key="view_items_button", use_container_width=True):
                    st.switch_page("pages/01_Consumer_Clothing_Items.py")
            
            with col2:
                if st.button("👔 View Outfits", key="view_outfits_button", use_container_width=True):
                    st.switch_page("pages/01_Consumer_Outfits.py")
            
            with col3:
                if st.button("🔄 Change Closet", key="change_closet_button", use_container_width=True):
                    st.session_state['closet_id'] = None
                    st.rerun()
        
    else:
        st.info("👆 Select a closet above to view its contents")

else:
    st.error("Unable to load closet data. Please try again later.")


# Sidebar Stats:
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Account Overview")
    
    if closet_data and closets:
        st.metric("Total Closets", len(closets))
        
        total_items = sum(c['items_count'] for c in closets.values())
        total_outfits = sum(c['outfits_count'] for c in closets.values())
        
        st.metric("Total Items", total_items)
        st.metric("Total Outfits", total_outfits)
        
        # Show largest closet
        if closets:
            largest_closet = max(closets.items(), key=lambda x: x[1]['items_count'])
            closet_names = {
                109: "Gym Bag", 110: "Office Fits", 111: "Date Night",
                112: "Casual", 113: "Summer 2025", 114: "Winter Vault",
                115: "Interview Clothes", 116: "Lounge"
            }
            largest_name = closet_names.get(largest_closet[0], f"Closet {largest_closet[0]}")
            
            st.markdown("**Largest Closet**")
            st.text(f"{largest_name}")
            st.text(f"({largest_closet[1]['items_count']} items)")
    
    st.markdown("---")
    
    if st.session_state.get('closet_id'):
        st.info(f"📂 Active: {st.session_state.get('closet_name', 'Closet')}")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()