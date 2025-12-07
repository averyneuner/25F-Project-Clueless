import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests


st.set_page_config(layout='wide')
SideBarLinks()


API_BASE_URL = "http://web-api:4000"


def get_top_wishlisted():
    """GET /analytics/analytics/demand"""
    try:
        resp = requests.get(f"{API_BASE_URL}/analytics/analytics/demand", timeout=10)
        return (True, resp.json()) if resp.status_code == 200 else (False, [])
    except:
        return False, []


st.title('Wishlist Matching Page')

if 'view' not in st.session_state:
    st.session_state.view = 'main'

if 'mapping_suggestions' not in st.session_state:
    st.session_state.mapping_suggestions = [
        {'item_name': 'White winter hood', 'wishlist_count': 36, 'business': 'Gucci', 'sku': '14Kp569', 'mapped': False},
        {'item_name': 'Black leather jacket', 'wishlist_count': 28, 'business': 'Gap', 'sku': '22Lj891', 'mapped': False},
        {'item_name': 'Blue denim jeans', 'wishlist_count': 24, 'business': 'Target Style', 'sku': '33Dj452', 'mapped': False},
    ]

if 'mapping_history' not in st.session_state:
    st.session_state.mapping_history = []


success, wishlisted_data = get_top_wishlisted()

def back_button():
    if st.button("← Back"):
        st.session_state.view = 'main'
        st.rerun()


if st.session_state.view == 'main':
    st.subheader('Wishlist Overview')
    
    if st.button("Top Wishlisted", use_container_width=True):
        st.session_state.view = 'top'
        st.rerun()
    if st.button("Unmatched Items", use_container_width=True):
        st.session_state.view = 'unmatched'
        st.rerun()
    if st.button("Mapping Suggestions", use_container_width=True):
        st.session_state.view = 'mapping'
        st.rerun()
    
    st.divider()
    st.subheader('Statistics')
    c1, c2 = st.columns(2)
    c1.metric("Top Wishlisted Items", len(wishlisted_data) if success else 0)
    unmatched_count = len([m for m in st.session_state.mapping_suggestions if not m['mapped']])
    c2.metric("Unmatched Items", unmatched_count)


elif st.session_state.view == 'top':
    back_button()
    st.title('Top Wishlisted')
    
    if success and wishlisted_data:
        for i, item in enumerate(wishlisted_data[:10]):
            rank = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"
            st.write(f"{rank} **{item.get('Name', 'Unknown')}** — Wishlists: {item.get('total_wishlists', 0)}")
            st.divider()
    else:
        st.info("No wishlist data available")


elif st.session_state.view == 'unmatched':
    back_button()
    st.title('Unmatched Items')
    
    unmatched = [m for m in st.session_state.mapping_suggestions if not m['mapped']]
    if unmatched:
        for item in unmatched:
            st.write(f"**{item['item_name']}** — Wishlists: {item['wishlist_count']}")
            st.caption("⚠️ Not mapped to any business SKU")
            st.divider()
    else:
        st.success("✅ All items have been mapped!")


elif st.session_state.view == 'mapping':
    back_button()
    st.title('Mapping Suggestions')
    
    if st.session_state.mapping_history:
        if st.button("↩️ Undo Last Mapping"):
            last = st.session_state.mapping_history.pop()
            for s in st.session_state.mapping_suggestions:
                if s['item_name'] == last:
                    s['mapped'] = False
            st.rerun()
    
    unmatched = [s for s in st.session_state.mapping_suggestions if not s['mapped']]
    
    if not unmatched:
        st.success("✅ All items have been mapped!")
    else:
        for s in unmatched:
            with st.container(border=True):
                st.write(f"**Item:** {s['item_name']}")
                st.write(f"**Business:** {s['business']} | **SKU:** {s['sku']}")
                if st.button("Map", key=s['item_name'], use_container_width=True, type="primary"):
                    s['mapped'] = True
                    st.session_state.mapping_history.append(s['item_name'])
                    st.rerun()