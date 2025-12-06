import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

API_BASE_URL=""

# Show sidebar links for the role of the user
SideBarLinks()

# Initialize the session state:
if 'selected_brand' not in st.session_state:
    st.session_state.selected_brand = 'American Eagle'

st.title("Brand View")
st.write('')
st.write('')

brands = ['ALO', 'H&M', 'American Eagle', 'Zara', 'PacSun']

brand_cols = st.columns(len(brands))


# Select
for i, brand in enumerate(brands):
    with brand_cols[i]:
        if st.button(brand, key=f"brand_{i}", use_container_width=True):
            st.session_state.selected_brand = brand
            st.toast(f"Viewing {brand}", icon='👀')

st.write('---')

col1, col2 = st.columns(2)

# Popularity With Users
with col1:
    st.header("Popularity With Users")
    st.write("**Last Year**")
    st.line_chart([180, 140, 160, 80, 100, 120, 140, 110, 130, 150])
    
    st.write("**Last Quarter**")
    st.line_chart([210, 160, 180, 90, 120, 140])

# Most Desired Items
with col2:
    st.header("Most Desired Items")
    
    items = [
        {"name": "Brannan Bear Sweater", "proj": "Rising Popularity", "sales": "70,123", "rev": "$123,456"},
        {"name": "Low Rise Baggy Jeans", "proj": "Rising Popularity", "sales": "123,456", "rev": "$78,910"},
        {"name": "Camisol Tank Top R", "proj": "Low Popularity", "sales": "123,456", "rev": "$78,910"},
        {"name": "Baggy T Shirts", "proj": "Low Popularity", "sales": "123,456", "rev": "$78,910"},
        {"name": "Racing Jackets", "proj": "Rising Popularity", "sales": "123,456", "rev": "$78,910"}
    ]
    
    for idx, item in enumerate(items):
        with st.expander(f"**{item['name']}**"):
            st.write(f"Projection: {item['proj']}")
            st.write(f"Sales: {item['sales']} | Revenue: {item['rev']}")
            if st.button(f"View Details", key=f"item_{idx}"):
                st.toast(f"Viewing {item['name']}", icon='📊')

