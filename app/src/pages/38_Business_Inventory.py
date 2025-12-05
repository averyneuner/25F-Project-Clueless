import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

# Defaults for Rebecca
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = 'Rebecca'

if 'business_name' not in st.session_state:
    st.session_state['business_name'] = "Rebecca's Vintage Closet"

st.title("📦 Full Inventory")
st.caption(f"All items for {st.session_state['business_name']}")

st.write("---")

# 🔹 Same dummy inventory data (later: replace with API call)
inventory_data = [
    {"Item ID": 820, "Item Name": "Vintage Silk Scarf", "Category": "Accessory", "Price": 120.00, "Size": "OneSize", "Qty in Stock": 12, "Units Sold (30d)": 34, "Ethically Sourced": "Yes"},
    {"Item ID": 821, "Item Name": "Faux Leather Skirt", "Category": "Skirt", "Price": 45.00, "Size": "S", "Qty in Stock": 8, "Units Sold (30d)": 10, "Ethically Sourced": "Yes"},
    {"Item ID": 825, "Item Name": "Oversized Denim Jacket", "Category": "Jacket", "Price": 75.00, "Size": "XL", "Qty in Stock": 5, "Units Sold (30d)": 18, "Ethically Sourced": "Yes"},
    {"Item ID": 837, "Item Name": "High Waisted Leggings", "Category": "Pants", "Price": 90.00, "Size": "S", "Qty in Stock": 20, "Units Sold (30d)": 50, "Ethically Sourced": "Yes"},
    {"Item ID": 842, "Item Name": "Velour Tracksuit", "Category": "Set", "Price": 80.00, "Size": "L", "Qty in Stock": 3, "Units Sold (30d)": 4, "Ethically Sourced": "No"},
    {"Item ID": 843, "Item Name": "Knee High Boots", "Category": "Shoes", "Price": 120.00, "Size": "7", "Qty in Stock": 8, "Units Sold (30d)": 2, "Ethically Sourced": "No"},
    {"Item ID": 844, "Item Name": "Baguette Bag", "Category": "Accessory", "Price": 200.00, "Size": "OneSize", "Qty in Stock": 10, "Units Sold (30d)": 1, "Ethically Sourced": "Yes"},
]

inv_df = pd.DataFrame(inventory_data)

# Optional: little filters at top
with st.expander("Filter inventory"):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        category_filter = st.multiselect(
            "Category",
            sorted(inv_df["Category"].unique()),
            default=None
        )
    with col_f2:
        ethical_filter = st.multiselect(
            "Ethically Sourced",
            ["Yes", "No"],
            default=None
        )

    filtered = inv_df.copy()
    if category_filter:
        filtered = filtered[filtered["Category"].isin(category_filter)]
    if ethical_filter:
        filtered = filtered[filtered["Ethically Sourced"].isin(ethical_filter)]
else:
    filtered = inv_df

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)