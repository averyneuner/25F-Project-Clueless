import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout= 'wide')

API_BASE_URL = "http://web-api:4000"

# API retrival functions: 

# 1) get the customer's closet

def get_customer_closet(customer_id):
    try: 
        response = requests.get(f"{API_BASE_URL}/customer/{customer_id}/closets", timeout=5)
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
    

# 2) add a clothing item to the closet
def add_item_to_closet(customer_id, closet_id, item_id):
    try:
        response = requests.post(
            f"{API_BASE_URL}/customer/{customer_id}/closets/{closet_id}/item/{item_id}"
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

# 3) creates a new clothing item with given information by the user
def create_clothing_item(item_data):
    try:
        response = requests.post(
            f"{API_BASE_URL}/items",
            json=item_data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Error creating item: {e.response.json().get('error', 'Unknown error')}")
        return None
    except Exception as e:
        st.error(f"❌ Error")
        return None

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

if 'customer_id' not in st.session_state:
    st.session_state['customer_id'] = 13
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
        padding: 5px 10 px;
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

st.title(f"👗 {st.session_state['first_name']}'s Closet")
st.markdown("View and manage your clothing items.")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Back to Closet", key="back_button"):
        st.switch_page("pages/00_Consumer_Closet.py")

st.divider()

# need to get the data:
closet_data = get_customer_closet(st.session_state['customer_id'])

if closet_data:
    items = closet_data.get('items', [])

    # case 1: when the closet is empty (no items yet)
    if not items:
        st.info("Your closet is empty. Add some items to get started!")

        with st.expander(" Add Your First Item", expanded= True):
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

                submit = st.form_submit_button("Create & Add to Closet")
                if submit:
                    if not all ([name, category, price, size, rating]):
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
                            add_result = add_item_to_closet(
                                st.session_state['customer_id'],
                                st.session_state['closet_id'],
                                new_item_id
                            )
                            if add_result:
                                st.success("🥳 Item added to your closet!")
                                st.rerun()
    
    # case 2: have clothing items in your closet:
    else:
        st.subheader(f"📦 Total Items: {len(items)}")

        col1, col2 = st.columns([2, 2])

        # filter by categories
        with col1:
            categories = sorted(list(set([item['Category'] for item in items])))
            selected_category = st.selectbox(
                "Filter by Category", 
                ["All Categories"] + categories,
                key="category_filter"
            )
        
        # filter by availability
        with col2:
            availability_options = ["All items", "Available", "Unavailable"]
            selected_availability = st.selectbox(
                "Filter by Availability",
                availability_options,
                key="availability_filter"
            )

    st.divider()

    filtered_items = items.copy()

    if selected_category != "All Categories":
        filtered_items = [item for item in filtered_items if item['Category'] == selected_category]

    if selected_availability == "Available Only":
        filtered_items = [item for item in filtered_items if item['AvailabilityStatus']]

    elif selected_availability == "Unavailable Only":
        filtered_items = [item for item in filtered_items if not item['AvailabilityStatus']]

    if not filtered_items: 
        st.warning("No items match your filters.")
    else:
        st.markdown(f"**Showing {len(filtered_items)} of {len(items)} items**")
        cols = st.columns(3)

        for idx, item in enumerate(filtered_items):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"### {item['ItemName']}")
                    st.markdown(
                        f'<span class="category_badge">{item["Category"]}</span>',
                        unsafe_allow_html=True
                    )

                    st.write("")

                    # Stats to display:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Times Worn", item['NumberofWears'])
                    with col_b:
                        if item['AvailabilityStatus']:
                            st.success("✅ Available")
                        else:
                            st.error("❎ Unavailable")
                    st.caption(f"Closet ID: {item['ClosetID']}")

    st.divider()

    with st.expander("➕ Add New Item to Closet"):
        tab1, tab2 = st.tabs(["Add Existing Item", "Create New Item"])

        # case 1: add an existing item to my closet (item already in db)
        with tab1:
            with st.form("add_existing_item"):
                st.markdown("**Add an item that already exists in the database**")
                item_id = st.number_input(
                    "Item ID",
                    min_value=1,
                    step=1,
                    help="Enter ID of an existing clothing item"
                )

                submit_existing = st.form_submit_button("Add to Closet")
                if submit_existing:
                    result = add_item_to_closet(
                        st.session_state['customer_id'],
                        st.session_state['closet_id'],
                        item_id
                    )
                    if result:
                        st.success(f"✅ Item added successfully!")
                        st.rerun()
        
        # case 2: add info for a new clothing item to be added to db
        with tab2:
            with st.form("create_new_item"):
                st.markdown("**Create a brand new item & add it to your closet**")

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

                submit_new = st.form_submit_button("Create & Add to Closet")
                    
                if submit_new:
                    if not all([name, category, price, size, rating]):
                        st.error("Need to fill in all required fields.")
                    else:
                        item_data = {
                            "name": name,
                            "category": category,
                            "price": price, 
                            "size": size,
                            "image": image
                        }

                        result = create_clothing_item(item_data)
                        if result:
                            new_item_id = result.get('ItemID')
                            st.success(f"✅ Item Created! (ID: {new_item_id})")

                            add_result = add_item_to_closet(
                                st.session_state['customer_id'],
                                st.session_state['closet_id'],
                                new_item_id
                            )
                            if add_result:
                                st.success("✅ Item added to your closet!")
                                st.rerun()
else:
    st.error("Unable to load closet data.")

# Some quick sidebar closet data stats:
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")

    if closet_data and items:
        total_items = len(items)
        available_items = len([i for i in items if i['AvailabilityStatus']])
        unavailable_items = total_items - available_items
        total_wears = sum([i['NumberofWears'] for i in items])
        categories = len(set([i['Category'] for i in items]))

        st.metric("Total Items", total_items)
        st.metric("Available", available_items)
        st.metric("Unavailable", unavailable_items)
        st.metric("Total Wears", total_wears)
        st.metric("Categories", categories)

        if items:
            most_worn = max(items, key=lambda x: x['NumberofWears'])
            st.markdown("**Most Worn Item**")
            st.text(f"{most_worn['ItemName']}")
            st.text(f"({most_worn['NumberofWears']} wears)")

    st.markdown("---")
    if st.button("🔄 Refresh Data"):
        st.rerun()