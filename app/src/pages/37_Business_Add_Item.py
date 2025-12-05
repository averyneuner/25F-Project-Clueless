import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Sidebar links
SideBarLinks()

# Use Rebecca defaults (temporary)
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = 'Rebecca'

if 'business_name' not in st.session_state:
    st.session_state['business_name'] = "Rebecca's Vintage Closet"

st.title("➕ Add New Item")
st.caption(f"{st.session_state['business_name']} — Inventory Management")

st.write("---")
st.subheader("Item Details")

# ----- Form -----
with st.form("add_item_form", clear_on_submit=True):
    item_name = st.text_input("Item Name", placeholder="e.g., Sequined NYE Top")
    category = st.selectbox(
        "Category",
        ["Top", "Pants", "Dress", "Shoes", "Jacket", "Skirt", "Accessory"]
    )
    price = st.number_input("Price ($)", min_value=0.00, step=1.00)
    size = st.selectbox(
        "Size",
        ["Small", "Medium", "Large"]
    )
    ethically_sourced = st.checkbox("Ethically Sourced?")

    st.write("---")
    quantity = st.number_input("Starting Quantity", min_value=0, step=1)

    submitted = st.form_submit_button("Save Item")

    if submitted:
        # For now, show local confirmation
        st.success(f"Added: {item_name} ({category}) — {price}$.")

        # Later: POST → API → add to BusinessInventoryItemStorage
        # TODO: requests.post(API_BASE_URL + "/business/items", json={...}