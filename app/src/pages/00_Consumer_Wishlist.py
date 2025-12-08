import logging
logger = logging.getLogger(__name__)
import streamlit as st
import time
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

API_BASE_URL = "http://web-api:4000"

# API retrieval functions: 

# 1) get the customer's wishlist
def get_customer_wishlist(customer_id):
    try: 
        response = requests.get(f"{API_BASE_URL}/customer/{customer_id}/wishlists", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend at {API_BASE_URL}. Is your Flask server running?")
        return None
    except requests.exceptions.Timeout:
        st.error(f"❌ Request timed out. Backend may be slow or not responding.")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            st.error(f"❌ Customer ID {customer_id} not found in database.")
        else:
            st.error(f"❌ HTTP Error: {e.response.status_code} - {e.response.json().get('error', 'Unknown error')}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error")
        return None

# 2) add a clothing item to the wishlist
def add_item_to_wishlist(customer_id, wishlist_id, item_id):
    try:
        response = requests.post(
            f"{API_BASE_URL}/customer/{customer_id}/wishlists/{wishlist_id}/items/{item_id}"
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Error adding item: {e.response.json().get('error', 'Unknown error')}")
        return None
    except Exception as e:
        st.error(f"❌ Error")
        return None

# 3) create a new clothing item
def create_clothing_item(item_data):
    try:
        response = requests.post(
            f"{API_BASE_URL}/items",
            json=item_data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Error creating item: {e.response.json().get('error', 'Unknown error')}")
        return None
    except Exception as e:
        st.error(f"❌ Error creating item")
        return None

# 4) move item from wishlist to closet
def move_to_closet(customer_id, closet_id, item_id):
    try:
        response = requests.post(
            f"{API_BASE_URL}/customer/{customer_id}/closets/{closet_id}/item/{item_id}"
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Error moving to closet: {e.response.json().get('error', 'Unknown error')}")
        return None
    except Exception as e:
        st.error(f"❌ Error moving to closet")
        return None

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

if 'customer_id' not in st.session_state:
    st.session_state['customer_id'] = 13
    st.session_state['wishlist_id'] = 212
    st.session_state['closet_id'] = 115
    st.session_state['first_name'] = 'Rachel'
    st.session_state['last_name'] = 'Green'
    st.session_state['email'] = 'rachel.green@example.com'

# styling w CSS:
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #A78BFA;
        color: #1E293B;
        border-radius: 20px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
    }
    .stButton > button:hover {
        background-color: #9370DB;
        color: #E2E8F0;
    }
    .item-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-bottom: 10px;
    }
    .category-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        background-color: #DDD6FE;
        color: #5B21B6;
        margin-right: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title(f"✨ {st.session_state['first_name']}'s Wishlist")
st.markdown("View and manage your wishlist items.")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Back to Home", key="back_button"):
        st.switch_page("pages/00_Consumer_Home.py")

st.divider()

# get the wishlist data:
wishlist_data = get_customer_wishlist(st.session_state['customer_id'])

if wishlist_data:
    items = wishlist_data.get('wishlist', [])

    for item in items:
        if 'Price' in item:
            item['Price'] = float(item['Price'])

    aesthetic_matches = wishlist_data.get('aesthetic_matches', [])

    # case 1: when the wishlist is empty (no items yet)
    if not items:
        st.info("Your wishlist is empty. Add some items to get started!")

        with st.expander("➕ Add Your First Item", expanded=True):
            with st.form("add_first_item"):
                col1, col2 = st.columns(2)

                with col1:
                    name = st.text_input("Item Name*", placeholder="e.g., Wide Leg Jeans")
                    category = st.selectbox(
                        "Category*",
                        ["Top", "Pants", "Dress", "Jacket", "Shoes", "Accessory", "Skirt", "Set"]
                    )
                    price = st.number_input("Price*", min_value=0.0, step=0.01, format="%.2f")

                with col2:
                    size = st.text_input("Size*", placeholder="e.g., M, 32, etc.")
                    rating = st.slider("Quality Rating*", 1, 10, 7)
                    image = st.text_input("Image Path", value="img/default.jpg")

                submit = st.form_submit_button("Create & Add to Wishlist")
                if submit:
                    if not all([name, category, price, size, rating]):
                        st.error("Need all required data to be filled in.")
                    else:
                        item_data = {
                            "name": name,
                            "category": category,
                            "price": price,
                            "size": size,
                            "rating": rating,
                            "image": image
                        }

                        result = create_clothing_item(item_data)
                        if result: 
                            new_item_id = result.get('ItemID')
                            add_result = add_item_to_wishlist(
                                st.session_state['customer_id'],
                                st.session_state['wishlist_id'],
                                new_item_id
                            )
                            if add_result:
                                st.success("🥳 Item added to your wishlist!")
                                st.rerun()
    
    # case 2: have wishlist items in your wishlist:
    else:
        st.subheader(f"💝 Total Items: {len(items)}")

        # Show aesthetic matches if available
        if aesthetic_matches:
            st.info(f"✨ {len(aesthetic_matches)} items match your closet's aesthetic!")

        st.divider()

        st.markdown(f"**Showing {len(items)} wishlist items**")
        cols = st.columns(3)

        for idx, item in enumerate(items):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"### {item['Name']}")
                    
                    st.write("")

                    # Stats to display:
                    st.metric("Price", "$%.2f" % float(item['Price']))
                    
                    if item.get('ImageAddress'):
                        st.caption(f"Image: {item['ImageAddress']}")
                    
                    st.write("")
                    
                    # Move to Closet button
                    item_id = item.get('ItemID')
                    if item_id and st.button("➡️ Move to Closet", key=f"move_{idx}_{item['Name']}"):
                        result = move_to_closet(
                            st.session_state['customer_id'],
                            st.session_state['closet_id'],
                            item_id
                        )
                        if result:
                            st.success(f"✅ {item['Name']} moved to closet!")
                            time.sleep(1.5)
                            st.rerun()

    st.divider()

    with st.expander(" ➕ Add New Item to Wishlist"):
        tab1, tab2 = st.tabs(["Add Existing Item", "Create New Item"])

        # case 1: add an existing item to my wishlist (item already in db)
        with tab1:
            with st.form("add_existing_item"):
                st.markdown("**Add an item that already exists in the database**")
                item_id = st.number_input(
                    "Item ID",
                    min_value=1,
                    step=1,
                    help="Enter ID of an existing clothing item"
                )

                submit_existing = st.form_submit_button("Add to Wishlist")
                if submit_existing:
                    result = add_item_to_wishlist(
                        st.session_state['customer_id'],
                        st.session_state['wishlist_id'],
                        item_id
                    )
                    if result:
                        st.success(f"✅ Item added successfully!")
                        time.sleep(1.5)
                        st.rerun()

        with tab2:
            with st.form("create_new_item"):
                st.markdown("**Create a brand new item & add it to your wishlist**")

                col1, col2 = st.columns(2)

                with col1:
                    name = st.text_input("Item Name*", placeholder="e.g. Wide Leg Jeans")
                    category = st.selectbox(
                        "Category*",
                        ["Top", "Pants", "Dress", "Jacket", "Shoes", "Accessory", "Skirt", "Set"]
                    )
                    price = st.number_input("Price*", min_value=0.0, step=0.1, format="%.2f")

                with col2:
                    size = st.text_input("Size*", placeholder="e.g. M, 32, etc")
                    rating = st.slider("Quality Rating*", 1, 10, 7)
                    image = st.text_input("Image Path", value="img/default.jpg")

                submit_new = st.form_submit_button("Create & Add to Wishlist")
                    
                if submit_new:
                    if not all([name, category, price, size, rating]):
                        st.error("Need to fill in all required fields.")
                    else:
                        item_data = {
                            "name": name,
                            "category": category,
                            "price": price, 
                            "size": size,
                            "rating": rating,
                            "image": image
                        }

                        result = create_clothing_item(item_data)
                        if result:
                            new_item_id = result.get('ItemID')
                            time.sleep(1.5)
                            st.success(f"✅ Item Created! (ID: {new_item_id})")

                            add_result = add_item_to_wishlist(
                                st.session_state['customer_id'],
                                st.session_state['closet_id'],
                                new_item_id
                            )
                            if add_result:
                                st.success("✅ Item added to your closet!")
                                time.sleep(1.5)
                                st.rerun()

else:
    st.error("Unable to load wishlist data.")

# Some quick sidebar wishlist data stats:
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")

    if wishlist_data and items:
        total_items = len(items)
        total_value = sum([i['Price'] for i in items])
        aesthetic_count = len(aesthetic_matches) if aesthetic_matches else 0

        st.metric("Total Items", total_items)
        st.metric("Total Value", f"${total_value:.2f}")
        st.metric("Aesthetic Matches", aesthetic_count)

        if items:
            most_expensive = max(items, key=lambda x: x['Price'])
            st.markdown("**Most Expensive Item**")
            st.text(f"{most_expensive['Name']}")
            st.text(f"(${most_expensive['Price']:.2f})")

    st.markdown("---")
    if st.button("🔄 Refresh Data"):
        time.sleep(1.5)
        st.rerun()