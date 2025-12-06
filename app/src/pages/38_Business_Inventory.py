import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

API_BASE = "http://web-api:4000"

SideBarLinks()

# -------------------------
# Session defaults
# -------------------------
if "first_name" not in st.session_state:
    st.session_state["first_name"] = "Rebecca"

if "business_name" not in st.session_state:
    st.session_state["business_name"] = "Rebecca's Vintage Closet"

# Rebecca = business 1 (you can change later if needed)
if "business_id" not in st.session_state:
    st.session_state["business_id"] = 1

business_id = st.session_state["business_id"]

st.title("📦 Full Inventory")
st.caption(f"All items for {st.session_state['business_name']}")
st.write("---")


# -------------------------
# Helper: load inventory from API
# -------------------------
def load_inventory_df(business_id: int) -> pd.DataFrame:
    url = f"{API_BASE}/business/business/{business_id}/inventory"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return pd.DataFrame(columns=[
            "ItemID", "Name", "Category", "Price", "QuantityInStock", "UnitsSold"
        ])
    df = pd.DataFrame(data)
    return df


inv_df = load_inventory_df(business_id)


# -------------------------
# Add existing ClothingItem to inventory
# -------------------------
with st.expander("➕ Add existing clothing item to this business's inventory"):
    st.markdown(
        "You must use a **valid InventoryID** and **existing ClothingItemID** "
        "from your database (BusinessInventory & ClothingItem tables)."
    )

    with st.form("add_inventory_item_form"):
        inventory_id = st.number_input(
            "InventoryID (from BusinessInventory)",
            min_value=1,
            step=1,
            format="%d",
        )
        item_id = st.number_input(
            "ClothingItemID (from ClothingItem)",
            min_value=1,
            step=1,
            format="%d",
        )
        qty = st.number_input(
            "Quantity In Stock",
            min_value=1,
            step=1,
            format="%d",
        )
        ethical = st.checkbox("Ethically Sourced?", value=False)

        submitted = st.form_submit_button("Add to Inventory")

        if submitted:
            payload = {
                "EthicallySourcedFlag": bool(ethical),
                "QuantityInStock": int(qty),
            }
            try:
                url = f"{API_BASE}/business/business/{business_id}/inventory/{int(inventory_id)}/item/{int(item_id)}"
                resp = requests.post(url, json=payload, timeout=5)

                if resp.status_code == 201:
                    st.success("✅ Item added to inventory!")
                    st.experimental_rerun()
                else:
                    # try to show API error message if present
                    try:
                        st.error(f"API error: {resp.status_code} {resp.json()}")
                    except Exception:
                        st.error(f"API error: {resp.status_code}")
            except Exception as e:
                st.error(f"Request failed: {e}")


st.write("---")

# -------------------------
# If no inventory rows yet
# -------------------------
if inv_df.empty:
    st.info("No inventory items found yet for this business.")
else:
    # -------------------------
    # Simple filters
    # -------------------------
    with st.expander("Filter inventory"):
        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.multiselect(
                "Category",
                sorted(inv_df["Category"].dropna().unique()),
            )
        with col2:
            # We don't have EthicallySourcedFlag in this GET route,
            # so we only filter by category for now.
            pass

    filtered = inv_df.copy()
    if "Category" in filtered.columns and category_filter:
        filtered = filtered[filtered["Category"].isin(category_filter)]

    st.write("### 🗂️ Inventory Items")

    # nice display names
    display_df = filtered.rename(
        columns={
            "ItemID": "Item ID",
            "Name": "Item Name",
            "Category": "Category",
            "Price": "Price",
            "QuantityInStock": "Qty in Stock",
            "UnitsSold": "Units Sold",
        }
    )

    # -------------------------
    # Table with delete buttons
    # -------------------------

    for _, row in filtered.iterrows():
        c1, c2, c3, c4, c5, c6 = st.columns([1.2, 3, 2, 1.5, 1.5, 1])

        # Display
        c1.write(int(row["ItemID"]))
        c2.write(str(row["Name"]))
        c3.write(str(row["Category"]))
        c4.write(row.get("Price", ""))
        c5.write(row.get("QuantityInStock", ""))

        # Unique key using InventoryID + ItemID (if InventoryID not returned, fallback)
        inventory_id = row.get("InventoryID", 0)
        item_id = int(row["ItemID"])
        key = f"del_{inventory_id}_{item_id}"

        if c6.button("🗑️", key=key):
            try:
                # call delete route using bridge item id
                del_url = f"{API_BASE}/business/business/{business_id}/inventory/{item_id}"
                resp = requests.delete(del_url, timeout=5)
                if resp.status_code == 200:
                    st.success(f"Removed {row['Name']} from inventory.")
                    st.experimental_rerun()
                else:
                    st.error(f"Delete failed: {resp.status_code}")
            except Exception as e:
                  st.error(f"Request failed: {e}")


    st.write("----")
    st.markdown("#### Raw inventory table")
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )
