import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

API_BASE_URL = ""

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title("Wish Lists")
st.write('')

# Create new wishlist button at top right
col_spacer, col_button = st.columns([4, 1])
with col_button:
    if st.button("+ Create New List", use_container_width=True):
        st.toast("Creating new wishlist", icon='✨')

st.write('---')

col1, col2 = st.columns(2)

# User Wishlists Overview + Most Wishlisted Items Section
with col1:
    st.subheader("User Wishlists Overview")
    
    stats_cols = st.columns(2)
    with stats_cols[0]:
        st.metric(label="Total Active Wishlists", value="2,847")
    
    with stats_cols[1]:
        st.metric(label="Total Items Wishlisted", value="34,592")
    
    st.write('')
    st.subheader("Most Wishlisted Items")
    
    items = [
        {"name": "Vintage Denim Jacket", "brand": "American Eagle", "users": "1,234"},
        {"name": "White Platform Sneakers", "brand": "Nike", "users": "1,098"},
        {"name": "Oversized Blazer Black", "brand": "Zara", "users": "987"},
        {"name": "Floral Maxi Dress", "brand": "H&M", "users": "856"}
    ]
    
    for idx, item in enumerate(items):
        with st.expander(f"**{item['name']}**"):
            st.write(f"{item['brand']} | {item['users']} users")
            if st.button(f"View Details", key=f"item_{idx}"):
                st.toast(f"Viewing {item['name']}", icon='👀')

# Wishlist Matching Opportunities
with col2:
    st.subheader("Wishlist Matching Opportunities")
    
    matches = [
        {"title": "🎯 High Match Rate", "info1": "342 users want Cargo Pants", "info2": "American Eagle has 15 in stock"},
        {"title": "🎯 Restock Alert", "info1": "256 users want Leather Boots", "info2": "Zara restocked yesterday"}
    ]
    
    for idx, match in enumerate(matches):
        st.success(match['title'])
        st.write(match['info1'])
        st.write(match['info2'])
        
        if st.button("Notify Users", key=f"notify_{idx}"):
            st.toast("Sending notifications!", icon='📧')
        st.write('')
    
    st.subheader("Wishlist Analytics")
    
    st.write("**Wishlist by Category**")
    category_data = {"Tops": 32, "Bottoms": 28, "Shoes": 24, "Accessories": 16}
    st.bar_chart(category_data)
    st.write("Avg items per wishlist: **12.1**")