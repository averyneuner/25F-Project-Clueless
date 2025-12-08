import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import requests


st.set_page_config(layout = 'wide')

API_BASE = "http://web-api:4000"

SideBarLinks()

# Title page:
st.header(f"Welcome back to {st.session_state['first_name']} 👋")

st.write("")  # little spacing


st.write("---")
st.subheader("Inventory Performance")

def load_inventory_df(business_id=40):
    url = f"{API_BASE}/business/{business_id}/inventory"
    
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()  # if API is bad -> throw
    
    data = resp.json()
    df = pd.DataFrame(data)
    
    df = df.rename(columns={
        "ItemID": "Item ID",
        "Name": "Item Name",
        "Category": "Category",
        "QuantityInStock": "Qty in Stock",
        "UnitsSold": "Units Sold (30d)",
    })
    return df

inv_df = load_inventory_df()

# sort for best and worst

if inv_df.empty or "Units Sold (30d)" not in inv_df.columns:
    st.info("No inventory data yet for this business. Add some items to the inventory first.")
else:
    # sort for best and worst
    top_sellers = inv_df.sort_values(
        by="Units Sold (30d)", ascending=False
    ).head(3)
    poor_sellers = inv_df.sort_values(
        by="Units Sold (30d)", ascending=True
    ).head(3)

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