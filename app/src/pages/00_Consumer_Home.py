import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

API_BASE_URL = "http://localhost:8501/"

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Initialize session state:
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = 'Guest'

if 'active_category' not in st.session_state:
    st.session_state.active_category = None

if 'active_occasion' not in st.session_state:
    st.session_state.active_occasion = None

# holds the ids of items user selects (temp "wishlist") before sent to backend on wishlist page.
if 'pending_wishlist_item_ids' not in st.session_state:
    st.session_state.pending_wishlist_item_ids = []

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')

# filler search bar (not fully functional yet)

search_bar = st.text_input (
    label="Find your next wardrobe addition",
    placeholder="🔍 Search...", 
    key="main_search_bar",
    label_visibility="collapsed")

if search_bar:
    st.write(f"You searched for: **{search_bar}**")

# Potential additions to your closet --> horizontal scrolling containers

st.header('Explore this season\'s necesities: 🛍️')

products = [
    {"id": 501, "image": "assets/cable_knit_sweater_beige.png", "caption": "Beige Cable Knit Sweater"},
    {"id": 502, "image": "assets/beige_quarter_zip.png", "caption": "Beige Quarter Zip"},
    {"id": 503, "image": "assets/maroon_cardigan.png", "caption": "Maroon Cardigan"},
    {"id": 504, "image": "assets/chocolate_sweater.png", "caption": "Chocolate Sweater"},
]

container = st.container()
with container:
    cols = st.columns(len(products))
   
   # style buttons:
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #A78BFA;
            color: #1E293B;
            border-radius: 20 px;
            padding: 5px 15px;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #9370DB;
            color: #E2E8F0;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    for i, col in enumerate(cols):
        product = products[i]
        with col: 
            st.image(product["image"], caption=product["caption"], width=150, output_format='auto')

            # add to wishlist button:
            if st.button(f"💜 Add to Wishlist", key=f"btn_{i}"):
                # TODO: REST API Call --> add item to wishlist
                item_id = product['id']

                if item_id not in st.session_state.pending_wishlist_item_ids:
                    st.session_state.pending_wishlist_item_ids.append(product['id'])
                    st.toast(f"{product['caption']} added to pending list!", icon='🥳')

                else:
                    st.toast(f"{product['caption']} is already pending!", icon='✅')

st.write('---')

# Browse by category --> badges
st.header('Browse by Category 👚')
categories = ['Sweaters', 'Jackets', 'Pants', 'Dresses', 'Accessories', 'Shoes']

cat_columns = st.columns(len(categories))
for i, cat in enumerate(categories):
    with cat_columns[i]:
        if st.button(f"{cat}", key=f"cat_{i}", width=250):
            # TODO: nav to filtered view/update data
            st.session_state.active_category = cat
            st.session_state.active_occasion = None
            st.info(f"Filtering by: **{st.session_state.active_category}**")

st.write('---')

# Explore by occasion --> badges
st.header('Explore by Occasion 🪩')

occasions = ['Casual', 'Work', 'Night Out', 'Formal', 'Gym']

occ_columns = st.columns(len(occasions))
for i, occasion_name in enumerate(occasions):
    with occ_columns[i]:
        if st.button(f"✨ {occasions[i]}", key=f"occ_{i}", width=150):
            # TODO: nav to filtered view/update data
            st.session_state.active_occasion = occasions[i]
            st.session_state.active_category = None
            st.info(f"Filtering by: **{st.session_state.active_occasion}**")

st.write('---')
