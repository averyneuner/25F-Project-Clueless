import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd

st.set_page_config(layout = 'wide')

API_BASE_URL = ""

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Initialize session state:
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = 'Guest'

if "role" not in st.session_state:
    st.session_state["role"] = "business_owner"

if 'active_category' not in st.session_state:
    st.session_state.active_category = None

if 'active_occasion' not in st.session_state:
    st.session_state.active_occasion = None

if 'business_name' not in st.session_state:
    st.session_state['business_name'] = "Rebecca's Boutique"

# Title page:
st.title(f"Business Profile — {st.session_state['business_name']}")
st.header(f"Welcome back, {st.session_state['first_name']} 👋")

st.write("")  # little spacing

st.write("---")
st.subheader("Inventory Performance")

# 🔹 Dummy inventory data (later: pull from API)
inventory_data = [
    {"Item ID": 820, "Item Name": "Vintage Silk Scarf", "Category": "Accessory", "Qty in Stock": 12, "Units Sold (30d)": 34},
    {"Item ID": 825, "Item Name": "Oversized Denim Jacket", "Category": "Jacket", "Qty in Stock": 5, "Units Sold (30d)": 18},
    {"Item ID": 837, "Item Name": "High Waisted Leggings", "Category": "Pants", "Qty in Stock": 20, "Units Sold (30d)": 50},
    {"Item ID": 842, "Item Name": "Velour Tracksuit", "Category": "Set", "Qty in Stock": 3, "Units Sold (30d)": 4},
    {"Item ID": 843, "Item Name": "Knee High Boots", "Category": "Shoes", "Qty in Stock": 8, "Units Sold (30d)": 2},
    {"Item ID": 844, "Item Name": "Baguette Bag", "Category": "Accessory", "Qty in Stock": 10, "Units Sold (30d)": 1},
]

inv_df = pd.DataFrame(inventory_data)

# sort for best and worst
top_sellers = inv_df.sort_values(by="Units Sold (30d)", ascending=False).head(3)
poor_sellers = inv_df.sort_values(by="Units Sold (30d)", ascending=True).head(3)

col_good, col_bad = st.columns(2)

with col_good:
    st.markdown("### 🔥 Top Sellers")
    st.dataframe(
        top_sellers[["Item Name", "Category", "Units Sold (30d)", "Qty in Stock"]],
        use_container_width=True,
        hide_index=True
    )

with col_bad:
    st.markdown("### 🥶 Selling Poorly")
    st.dataframe(
        poor_sellers[["Item Name", "Category", "Units Sold (30d)", "Qty in Stock"]],
        use_container_width=True,
        hide_index=True
    )

st.caption("Tip: Use this to help determine what to restock, promote, or discount.")

inv_df = pd.DataFrame(inventory_data)

st.dataframe(
    inv_df,
    use_container_width=True,
    hide_index=True
)

st.write("")
st.subheader("Quick Actions")

a_col1, a_col2 = st.columns(2)

with a_col1:
    if st.button("➕ Add New Item", use_container_width=True):
        st.info("Later: open a form to create a new inventory item.")

with a_col2:
    if st.button("📦 Restock Low Inventory", use_container_width=True):
        st.info("Later: call API to update QuantityInStock for selected items.")
