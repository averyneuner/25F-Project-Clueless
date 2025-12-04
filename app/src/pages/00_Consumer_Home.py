import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')

st.header('Explore this season\'s necesities:')

# Potential additions to your closet --> horizontal scrolling containers



container = st.container()
with container:
    col1, col2, col3, col4 = st.columns(4, 4, 4, 4)
    for i, col in enumerate(col):
        with "col{i}":
            # styling button:
            st.markDown(
                """
                <style>
                .stButton > button {
                    background-color: #A78BFA; #lavender background
                    color: #1E293B; #navy text
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"💜", key=f"btn_{i}"):
                st.success(f"Added to Wishlist!", st.button("View", key=f""))
    with col1:
        st.image("assets/cable_knit_sweater_beige.png", caption="Beige Cable Knit Sweater")
        st.button()
    with col2:
        st.image("assets/beige_quarter_zip.png", caption="Beige Quarter Zip")
    with col3:
        st.image("assets/maroon_cardigan.png", caption="Maroon Cardigan")
    with col4:
        st.image("assets/chocolate_sweater.png", caption="Chocolate Sweater")
# TO DO: browse by category --> badges

# TO DO: explore by occasion --> badges