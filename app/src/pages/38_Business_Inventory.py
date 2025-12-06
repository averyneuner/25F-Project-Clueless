import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

API_BASE = "http://web-api:4000"

SideBarLinks()

# Session defaults
if "first_name" not in st.session_state:
    st.session_state["first_name"] = "Rebecca"

if "business_name" not in st.session_state:
    st.session_state["business_name"] = "Rebecca's Vintage Closet"

if "business_id" not in st.session_state:
    st.session_state["business_id"] = 1

business_id = st.session_state["business_id"]

st.title("📦 Full Inventory")
st.caption(f"All items for {st.session_state['business_name']}")
st.write("---")


# Helpers
def load_inventory_df(business_id: int) -> pd.DataFrame:
    """
    Call GET /business/business/<business_id>/inventory
    and return a DataFrame with the raw columns from the API.
    """
    url = f"{API_BASE}/business/business/{business_id}/inventory"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return pd.DataFrame(
                columns=[
                    "ItemID",
                    "Name",
                    "Category",
                    "Price",
                    "QuantityInStock",
                    "UnitsSold",
                ]
            )
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Could not load inventory from the API: {e}")
        return pd.DataFrame(
            columns=[
                "ItemID",
                "Name",
                "Category",
                "Price",
                "QuantityInStock",
                "UnitsSold",
            ]
        )


def add_inventory_item(
    business_id: int,
    inventory_id: int,
    clothing_item_id: int,
    qty_in_stock: int,
    ethically_sourced: bool,
):
    """
    Call POST /business/business/<business_id>/inventory/<inventory_id>/item/<clothing_item_id>
    using the route defined in clueless_routes.py.
    """
    url = (
        f"{API_BASE}/business/business/"
        f"{business_id}/inventory/{inventory_id}/item/{clothing_item_id}"
    )
    payload = {
        "EthicallySourcedFlag": bool(ethically_sourced),
        "QuantityInStock": int(qty_in_stock),
    }
    try:
        resp = requests.post(url, json=payload, timeout=5)
        if resp.status_code == 201:
            return True, "Item added to inventory."
        else:
            try:
                return False, f"API error {resp.status_code}: {resp.json()}"
            except Exception:
                return False, f"API error {resp.status_code}"
    except Exception as e:
        return False, f"Request failed: {e}"


def delete_inventory_item(business_id: int, clothing_item_id: int):
    """
    Call DELETE /business/business/<business_id>/inventory/<clothing_item_id>
    which deletes rows in BusinessInventoryItemStorage for that ClothingItemID.
    """
    url = f"{API_BASE}/business/business/{business_id}/inventory/{clothing_item_id}"
    try:
        resp = requests.delete(url, timeout=5)
        if resp.status_code == 200:
            return True, "Item removed from inventory."
        else:
            try:
                return False, f"API error {resp.status_code}: {resp.json()}"
            except Exception:
                return False, f"API error {resp.status_code}"
    except Exception as e:
        return False, f"Request failed: {e}"


# Load current inventory
inv_df = load_inventory_df(business_id)


# Add existing ClothingItem to inventory
with st.expander("➕ Add existing clothing item to this business's inventory"):
    st.markdown(
        "Use an **InventoryID** from the `BusinessInventory` table and a "
        "**ClothingItemID** from the `ClothingItem` table."
    )

    with st.form("add_inventory_item_form"):
        inventory_id_input = st.number_input(
            "InventoryID (from BusinessInventory)",
            min_value=1,
            step=1,
            format="%d",
            value=1001, 
        )
        clothing_item_id_input = st.number_input(
            "ClothingItemID (from ClothingItem)",
            min_value=1,
            step=1,
            format="%d",
        )
        qty_input = st.number_input(
            "Quantity In Stock",
            min_value=1,
            step=1,
            format="%d",
            value=10,
        )
        ethical_input = st.checkbox("Ethically sourced?", value=True)

        submitted_add = st.form_submit_button("Add to Inventory")

        if submitted_add:
            ok, msg = add_inventory_item(
                business_id=business_id,
                inventory_id=int(inventory_id_input),
                clothing_item_id=int(clothing_item_id_input),
                qty_in_stock=int(qty_input),
                ethically_sourced=bool(ethical_input),
            )
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

st.write("---")

# If no inventory rows yet
if inv_df.empty:
    st.info("No inventory items found yet for this business.")
else:
    # Simple filters
    with st.expander("Filter inventory"):
        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.multiselect(
                "Category",
                sorted(inv_df["Category"].dropna().unique()),
            )
        with col2:
            st.caption(
                "Ethically sourced filtering would require that flag in the GET route; "
                "for now we only filter by category."
            )

    filtered = inv_df.copy()
    if "Category" in filtered.columns and category_filter:
        filtered = filtered[filtered["Category"].isin(category_filter)]

    st.write("### 🗂️ Inventory Items")

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

    # Display inventory items with delete buttons

    st.markdown("#### Editable list")

    if "recently_deleted_items" not in st.session_state:
        st.session_state["recently_deleted_items"] = []

    for idx, (_, row) in enumerate(filtered.iterrows()):
        c1, c2, c3, c4, c5, c6 = st.columns([1.2, 3, 2, 1.5, 1.5, 1])

        clothing_item_id = int(row["ItemID"])
        item_name = str(row["Name"])

        c1.write(clothing_item_id)
        c2.write(item_name)
        c3.write(str(row["Category"]))
        c4.write(row.get("Price", ""))
        c5.write(row.get("QuantityInStock", ""))

        btn_key = f"del_{idx}_{clothing_item_id}"

        if c6.button("🗑️", key=btn_key):
            ok, msg = delete_inventory_item(
                business_id=business_id,
                clothing_item_id=clothing_item_id,
            )
            if ok:
                deleted = st.session_state.get("recently_deleted_items", [])
                deleted.append(
                    {
                        "ItemID": clothing_item_id,
                        "Name": item_name,
                        "Category": row.get("Category", ""),
                    }
                )
                st.session_state["recently_deleted_items"] = deleted
                st.success(f"Removed '{item_name}' from inventory.")
                st.rerun()
            else:
                st.error(msg)

    st.write("---")
    st.markdown("#### Raw inventory table")
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

st.write("---")

# Add back items removed 

st.subheader("↩️ Add back items removed")

deleted_items = st.session_state.get("recently_deleted_items", [])

if not deleted_items:
    st.info(
        "No items have been removed from inventory during this session yet. "
        "When you delete an item above, it will appear here so you can add it back."
    )
else:
    options = [
        f"{item['Name']} (ID {item['ItemID']}, {item['Category']})"
        for item in deleted_items
    ]
    label_to_item = {label: item for label, item in zip(options, deleted_items)}

    selected_label = st.selectbox(
        "Select an item to add back to inventory:",
        options=options,
        index=0,
        key="add_back_select",
    )
    selected_item = label_to_item[selected_label]
    clothing_item_id_back = int(selected_item["ItemID"])

    st.markdown(
        f"**Selected:** {selected_item['Name']}  "
        f"(ItemID: `{clothing_item_id_back}`, Category: {selected_item['Category']})"
    )

    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        inventory_id_back = st.number_input(
            "Inventory ID to add into",
            min_value=1,
            step=1,
            value=1001,  
            key="inv_back_id",
        )
    with col_a2:
        qty_in_stock_back = st.number_input(
            "Quantity in Stock",
            min_value=0,
            step=1,
            value=10,
            key="qty_back",
        )
    with col_a3:
        ethically_sourced_back = st.checkbox(
            "Ethically sourced?", value=True, key="eth_back"
        )

    if st.button("➕ Add Back to Inventory", use_container_width=True, key="btn_add_back"):
        ok, msg = add_inventory_item(
            business_id=business_id,
            inventory_id=int(inventory_id_back),
            clothing_item_id=clothing_item_id_back,
            qty_in_stock=int(qty_in_stock_back),
            ethically_sourced=bool(ethically_sourced_back),
        )
        if ok:
            st.success(msg)
            # Remove it from the local "recently deleted" list
            st.session_state["recently_deleted_items"] = [
                d for d in deleted_items if d["ItemID"] != clothing_item_id_back
            ]
            st.rerun()
        else:
            st.error(f"Could not add item back: {msg}")
