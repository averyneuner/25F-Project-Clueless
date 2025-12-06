import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

API_BASE_URL = "http://web-api:4000"  

def get_business_id() -> int:
    return st.session_state.get("business_id", 1)

def get_wishlist_id() -> int:
    return st.session_state.get("wishlist_id", 1)

# ----------------- HELPERS (API CALLS) -----------------

def fetch_available_items(business_id: int):
    """
    Uses: GET /business/{business_id}/inventory/available
    Returns catalog items that are NOT in the business's inventory.
    """
    url = f"{API_BASE_URL}/business/{business_id}/inventory/available"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json(), None
    except requests.RequestException as e:
        return [], str(e)


def fetch_wishlist_items(business_id: int, wishlist_id: int):
    url = f"{API_BASE_URL}/business/{business_id}/wishlists/{wishlist_id}"
    try:
        resp = requests.get(url, timeout=5)

        # If the endpoint doesn't exist yet or returns 404 HTML,
        # don't try to parse it as JSON.
        if resp.status_code == 404:
            return [], f"Wishlist route not found (404) at {url}"

        # For any non-200 code, return a readable error message
        if resp.status_code != 200:
            return [], f"{resp.status_code} {resp.reason} for url: {url}"

        # Now it's safe to parse JSON
        return resp.json(), None

    except requests.RequestException as e:
        return [], str(e)
    except ValueError:
        # JSON decode failed
        return [], "API did not return valid JSON for wishlist items"


def add_item_to_wishlist(business_id: int, wishlist_id: int, item_id: int):
    """
    Uses: POST /business/{business_id}/wishlists/{wishlist_id}/item/{item_id}
    """
    url = f"{API_BASE_URL}/business/{business_id}/wishlists/{wishlist_id}/item/{item_id}"
    try:
        # API doesn't use the body, but sending an empty JSON is fine
        resp = requests.post(url, json={}, timeout=5)
        if resp.status_code >= 400:
            try:
                data = resp.json()
                return False, data.get("error", f"HTTP {resp.status_code}")
            except Exception:
                return False, f"HTTP {resp.status_code}"
        return True, None
    except requests.RequestException as e:
        return False, str(e)


def remove_item_from_wishlist(business_id: int, wishlist_id: int, item_id: int):
    """
    Uses: DELETE /business/{business_id}/wishlists/{wishlist_id}/item/{item_id}
    """
    url = f"{API_BASE_URL}/business/{business_id}/wishlists/{wishlist_id}/item/{item_id}"
    try:
        resp = requests.delete(url, timeout=5)
        if resp.status_code >= 400:
            try:
                data = resp.json()
                return False, data.get("error", f"HTTP {resp.status_code}")
            except Exception:
                return False, f"HTTP {resp.status_code}"
        return True, None
    except requests.RequestException as e:
        return False, str(e)


# ----------------- STREAMLIT PAGE -----------------

st.set_page_config(page_title="Business Wishlist", page_icon="📝", layout="wide")

# If you have a sidebar helper, call it:
# SideBarLinks()

# Basic session defaults so page doesn't explode
if "first_name" not in st.session_state:
    st.session_state["first_name"] = "Guest"

if "role" not in st.session_state:
    st.session_state["role"] = "business_owner"

# You can store / override these in session_state from your login/home page
business_id = get_business_id()
wishlist_id = get_wishlist_id()

st.title("Business Wishlist 📝")

st.caption(
    f"Business ID: `{business_id}` • Wishlist ID: `{wishlist_id}` "
    "(you can set these in session_state from your home/login page)."
)

# --- Load data from API ---
available_items, avail_err = fetch_available_items(business_id)
wishlist_items, wishlist_err = fetch_wishlist_items(business_id, wishlist_id)

if avail_err:
    st.error(f"Could not load available items: {avail_err}")

if wishlist_err and wishlist_items == []:
    # If wishlist doesn't exist yet, show the message but still let them try adding
    st.warning(f"Wishlist info: {wishlist_err}")

left, right = st.columns(2)

# ========== LEFT: Available items to add ==========
with left:
    st.subheader("Available Catalog Items (Not in Inventory)")

    if not available_items:
        st.info("No additional catalog items available to add to wishlist.")
    else:
        for item in available_items:
            # Expected JSON from /inventory/available:
            # ItemID, Name, Category, Price
            item_id = item.get("ItemID")
            name = item.get("Name")
            category = item.get("Category")
            price = item.get("Price")

            with st.container(border=True):
                st.markdown(f"**{name}**")
                st.caption(f"Category: {category} • Price: ${price}")

                if st.button(
                    "➕ Add to wishlist",
                    key=f"add_{item_id}",
                    use_container_width=True,
                    type="primary",
                ):
                    ok, err = add_item_to_wishlist(business_id, wishlist_id, item_id)
                    if ok:
                        st.success("Item added to wishlist.")
                        st.rerun()
                    else:
                        st.error(f"Could not add item to wishlist: {err}")

# ========== RIGHT: Current wishlist contents ==========
with right:
    st.subheader("Current Wishlist Items")

    if not wishlist_items:
        st.info("No items on this wishlist yet.")
    else:
        # enumerate gives us a unique index for each item
        for idx, item in enumerate(wishlist_items):
            # From GET /business/{business_id}/wishlists/{wishlist_id}:
            item_id = item.get("ItemID")
            name = item.get("Name")
            category = item.get("Category")
            price = item.get("Price")

            with st.container(border=True):
                st.markdown(f"**{name}**")
                st.caption(f"Category: {category} • Price: ${price}")

                # Unique key = index + item id
                if st.button(
                    "🗑 Remove from wishlist",
                    key=f"remove_{idx}_{item_id}",
                    use_container_width=True,
                ):
                    ok, err = remove_item_from_wishlist(business_id, wishlist_id, item_id)
                    if ok:
                        st.success("Item removed from wishlist.")
                        st.rerun()
                    else:
                        st.error(f"Could not remove item from wishlist: {err}")