import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

API_BASE_URL = ""

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Initialize session state
if 'time_period' not in st.session_state:
    st.session_state.time_period = 'This Week'

st.title("Trending")
st.write('')

# Time period filter buttons
st.write("Time Period:")

time_periods = ['This Week', 'This Month', 'This Year']

period_cols = st.columns(len(time_periods))

# Style time period buttons
for i, period in enumerate(time_periods):
    with period_cols[i]:
        if st.button(period, key=f"period_{i}", use_container_width=True):
            st.session_state.time_period = period

st.write('---')

col1, col2 = st.columns(2)

# Top Trending Items Section
with col1:
    st.subheader("Top Trending Items")
    
    items = [
        {"rank": 1, "name": "Oversized Blazers", "inc": "245%", "searches": "15,423", "wish": "3,200"},
        {"rank": 2, "name": "Wide Leg Jeans", "inc": "198%", "searches": "12,890", "wish": "2,800"},
        {"rank": 3, "name": "Platform Sneakers", "inc": "156%", "searches": "9,567", "wish": "2,100"},
        {"rank": 4, "name": "Crop Cardigans", "inc": "134%", "searches": "8,234", "wish": "1,900"},
        {"rank": 5, "name": "Maxi Skirts", "inc": "121%", "searches": "7,890", "wish": "1,700"}
    ]
    
    for item in items:
        with st.expander(f"**{item['rank']}. {item['name']}** - ↑ {item['inc']}"):
            st.write(f"Searches: {item['searches']} | Wishlisted: {item['wish']}")
            if st.button(f"View Details", key=f"trend_{item['rank']}"):
                st.toast(f"Viewing {item['name']}", icon='🔥')

# Trending By Category
with col2:
    st.subheader("Trending by Category")
    
    categories = {
        "Outerwear": 89, "Bottoms": 76, "Shoes": 65, "Tops": 54,
        "Dresses": 43, "Accessories": 38, "Jewelry": 27, "Bags": 22
    }
    
    st.bar_chart(categories)
    
    st.write('')
    st.subheader("Rising Stars 🌟")
    
    stars = [
        {"name": "Y2K Aesthetic", "inc": "312%"},
        {"name": "Cottagecore", "inc": "267%"},
        {"name": "Dark Academia", "inc": "189%"}
    ]
    
    star_cols = st.columns(3)
    for i, star in enumerate(stars):
        with star_cols[i]:
            st.metric(label=star['name'], value=f"↑ {star['inc']}")