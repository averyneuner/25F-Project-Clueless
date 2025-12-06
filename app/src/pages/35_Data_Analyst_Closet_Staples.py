import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

API_BASE_URL = ""

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Initialize session state
if 'view_filter' not in st.session_state:
    st.session_state.view_filter = 'All Items'

st.title("Closet Staples")
st.write('')
st.write("View by:")

filters = ['All Items', 'Essential Only', 'Seasonal']
filter_cols = st.columns(len(filters))

for i, view_filter in enumerate(filters):
    with filter_cols[i]:
        if st.button(view_filter, key=f"filter_{i}", use_container_width=True):
            st.session_state.view_filter = view_filter

st.write('---')
st.header("Essential Closet Staples")

items = [
    {"name": "White T-Shirt", "owned": "89%", "uses": "42/year", "rating": "4.8"},
    {"name": "Blue Jeans", "owned": "95%", "uses": "67/year", "rating": "4.9"},
    {"name": "Black Blazer", "owned": "76%", "uses": "34/year", "rating": "4.7"},
    {"name": "White Sneakers", "owned": "88%", "uses": "58/year", "rating": "4.6"},
    {"name": "Black Dress", "owned": "82%", "uses": "28/year", "rating": "4.8"},
    {"name": "Trench Coat", "owned": "64%", "uses": "22/year", "rating": "4.5"},
    {"name": "Leather Bag", "owned": "71%", "uses": "156/year", "rating": "4.9"},
    {"name": "Watch", "owned": "68%", "uses": "312/year", "rating": "4.7"}
]

cols = st.columns(4)
for idx, item in enumerate(items):
    with cols[idx % 4]:
        with st.expander(f"**{item['name']}**"):
            st.write(f"Owned by: {item['owned']}")
            st.write(f"Avg uses: {item['uses']}")
            st.write(f"Rating: ⭐ {item['rating']}")
            if st.button("Details", key=f"staple_{idx}"):
                st.toast(f"Viewing {item['name']}", icon='👕')

st.write('---')

col1, col2 = st.columns(2)

with col1:
    st.subheader("Usage Insights")
    st.write("**Most Worn Items (Last 30 Days)**")
    
    usage = {"Blue Jeans": 89, "White Sneakers": 76, "White T-Shirt": 63, "Black Blazer": 51}
    st.bar_chart(usage)

with col2:
    st.subheader("Missing Staples Recommendations")
    st.write("**Suggested additions:**")
    
    st.info("💡 **Neutral Cardigan** - Completes 87% of your outfits")
    st.info("💡 **Chelsea Boots** - Versatile for 73% of occasions")
