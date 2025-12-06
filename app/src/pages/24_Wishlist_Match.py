import logging
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()


if 'view' not in st.session_state:
    st.session_state.view = 'main'

if 'mapping_suggestions' not in st.session_state:
    st.session_state.mapping_suggestions = [
        {'item_name': 'White winter hood', 'wishlist_count': 36, 'business': 'Zara International', 'sku': '14Kp569', 'mapped': False},
        {'item_name': 'Black leather jacket', 'wishlist_count': 28, 'business': 'H&M Group', 'sku': '22Lj891', 'mapped': False},
        {'item_name': 'Blue denim jeans', 'wishlist_count': 24, 'business': 'Gap Inc.', 'sku': '33Dj452', 'mapped': False},
        {'item_name': 'Floral summer dress', 'wishlist_count': 19, 'business': 'Forever 21', 'sku': '44Fd783', 'mapped': False},
        {'item_name': 'Cashmere sweater', 'wishlist_count': 15, 'business': 'Uniqlo', 'sku': '55Cs126', 'mapped': False},
    ]

if 'mapping_history' not in st.session_state:
    st.session_state.mapping_history = []


TOP_WISHLISTED = [
    {'Name': 'High Waisted Leggings', 'total_wishlists': 45},
    {'Name': 'Combat Boots', 'total_wishlists': 38},
    {'Name': 'Lace Corset Top', 'total_wishlists': 32},
    {'Name': 'Oversized Denim Jacket', 'total_wishlists': 29},
    {'Name': 'High Top Sneakers', 'total_wishlists': 25},
]



def back_button():
    if st.button("← Back"):
        st.session_state.view = 'main'
        st.rerun()

# MAIN VIEW
if st.session_state.view == 'main':
    st.title('Wishlist Matching Page')
    st.subheader('Wishlist Overview')
    
    if st.button("🏆 Top Wishlisted", use_container_width=True):
        st.session_state.view = 'top'
        st.rerun()
    if st.button("❓ Unmatched Items", use_container_width=True):
        st.session_state.view = 'unmatched'
        st.rerun()
    if st.button("🔗 Mapping Suggestions", use_container_width=True):
        st.session_state.view = 'mapping'
        st.rerun()
    
    st.divider()
    st.subheader('📊 Statistics')
    c1, c2 = st.columns(2)
    c1.metric("Inventory Added", 12)
    c2.metric("New Collection in Pipeline", 8)

# TOP WISHLISTED VIEW
elif st.session_state.view == 'top':
    back_button()
    st.title('🏆 Top Wishlisted')
    
    for i, item in enumerate(TOP_WISHLISTED):
        rank = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"
        st.write(f"{rank} **{item['Name']}** — Wishlists: {item['total_wishlists']}")
        st.divider()

# UNMATCHED VIEW
elif st.session_state.view == 'unmatched':
    back_button()
    st.title('❓ Unmatched Items')
    
    unmatched = [m for m in st.session_state.mapping_suggestions if not m.get('mapped')]
    if unmatched:
        for item in unmatched:
            st.write(f"**{item['item_name']}** — Wishlists: {item['wishlist_count']}")
            st.write("⚠️ Not mapped to any business SKU")
            st.divider()
    else:
        st.success("✅ All items have been mapped!")

# MAPPING VIEW
elif st.session_state.view == 'mapping':
    back_button()
    st.title('🔗 Mapping Suggestions')
    
    if st.session_state.mapping_history:
        if st.button("↩️ Undo Last Mapping"):
            last_item = st.session_state.mapping_history.pop()
            for s in st.session_state.mapping_suggestions:
                if s['item_name'] == last_item:
                    s['mapped'] = False
            st.rerun()
    
    unmatched = [s for s in st.session_state.mapping_suggestions if not s.get('mapped')]
    
    if not unmatched:
        st.success("✅ All items have been mapped!")
    else:
        for s in unmatched:
            with st.container(border=True):
                st.write(f"**Item:** {s['item_name']}")
                st.write(f"**Business:** {s['business']}")
                st.write(f"**SKU:** {s['sku']}")
                if st.button("Map", key=s['item_name'], use_container_width=True, type="primary"):
                    s['mapped'] = True
                    st.session_state.mapping_history.append(s['item_name'])
                    st.rerun()