import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE_URL = "http://web-api:4000"



if 'admins' not in st.session_state:
    st.session_state.admins = [
        {'name': 'Lucas Fu', 'user_id': '16022006', 'role': 'Super Admin'},
        {'name': 'Alvin Wong', 'user_id': '11112005', 'role': 'Content Moderator'}
    ]

if 'admin_history' not in st.session_state:
    st.session_state.admin_history = []

if 'usage_violations' not in st.session_state:
    st.session_state.usage_violations = [
        {'name': 'Nisha Vernekar', 'user_id': 'MD9877', 'reason': 'Invalid email'},
        {'name': 'Janet Chen', 'user_id': 'JC1234', 'reason': 'Password Violation'}
    ]



st.title('Settings & Permissions Page')

tab1, tab2 = st.tabs(["Admin Management", "Remove Usage Access"])


with tab1:
    st.write("")
    
    # Add Admin Section
    st.subheader('Add Admin')
    
    with st.form("add_admin_form"):
        st.write("**Name**")
        admin_name = st.text_input("Name", value="", placeholder="Chayapa", label_visibility="collapsed")
        
        st.write("**User ID**")
        admin_user_id = st.text_input("User ID", value="", placeholder="000000000", label_visibility="collapsed")
        
        st.write("**Admin Roles**")
        admin_role = st.selectbox(
            "Admin Roles",
            ["Super Admin / Content Moderator...", "Super Admin", "Content Moderator", "Data Analyst", "Support Staff"],
            label_visibility="collapsed"
        )
        
        st.write("")
        
        submitted = st.form_submit_button("Add", use_container_width=True, type="primary")
        
        if submitted:
            if admin_name and admin_user_id and admin_role != "Super Admin / Content Moderator...":
                new_admin = {
                    'name': admin_name,
                    'user_id': admin_user_id,
                    'role': admin_role
                }
                st.session_state.admins.append(new_admin)
                st.success(f"Admin {admin_name} has been added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields")
    
    st.divider()
    
    # Remove Admin Section
    st.subheader('Remove Admin')
    
    # Undo button
    if st.session_state.admin_history:
        if st.button("↩️ Undo Last Delete"):
            last_admin = st.session_state.admin_history.pop()
            st.session_state.admins.append(last_admin)
            st.success(f"Restored {last_admin['name']}")
            st.rerun()
    
    search_admin = st.text_input("Search Admin", placeholder="🔍 Search", label_visibility="collapsed")
    st.caption("Search by Name or User ID")
    
    st.write("")
    
    # Display current admins
    if st.session_state.admins:
        st.write("**Current Admins:**")
        for admin in st.session_state.admins:
            # Filter by search
            if search_admin:
                if search_admin.lower() not in admin['name'].lower() and search_admin not in admin['user_id']:
                    continue
            
            with st.container(border=True):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.write(f"**{admin['name']}**")
                    st.write(f"ID: {admin['user_id']} • Role: {admin['role']}")
                with col2:
                    if st.button("❌", key=f"remove_admin_{admin['user_id']}"):
                        st.session_state.admin_history.append(admin)
                        st.session_state.admins = [a for a in st.session_state.admins if a['user_id'] != admin['user_id']]
                        st.success(f"Removed {admin['name']}")
                        st.rerun()
    
    st.write("")
    
    if st.button("Remove", use_container_width=True, disabled=not search_admin):
        found = False
        for admin in st.session_state.admins:
            if search_admin.lower() in admin['name'].lower() or search_admin == admin['user_id']:
                st.session_state.admin_history.append(admin)
                st.session_state.admins = [a for a in st.session_state.admins if a['user_id'] != admin['user_id']]
                st.success(f"Removed {admin['name']}")
                found = True
                st.rerun()
                break
        if not found:
            st.warning("Admin not found")


with tab2:
    st.write("")
    
    st.markdown("### Alerts ⚠️")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write("**Users with usage violation**")
    with col2:
        violation_count = len(st.session_state.usage_violations)
        if violation_count > 0:
            st.markdown(f"<span style='background-color:#EF4444;color:white;padding:2px 10px;border-radius:50%;font-size:14px;'>{violation_count}</span>", unsafe_allow_html=True)
    
    st.write("")
    
    for violation in st.session_state.usage_violations:
        with st.container(border=True):
            col1, col2, col3 = st.columns([0.5, 0.5, 8])
            with col1:
                st.markdown("🔴")
            with col2:
                st.markdown("👤")
            with col3:
                st.write(f"**{violation['name']}**")
                st.write(f"User ID: {violation['user_id']} • Reason: {violation['reason']}")
    
    st.write("")
    
    st.subheader('User search')
    
    search_user = st.text_input("Search User", placeholder="🔍 Search", label_visibility="collapsed", key="search_violation")
    st.caption("Search by Name or User ID")
    
    st.write("")
    
    if st.button("Remove", use_container_width=True, key="remove_user_access"):
        if search_user:
            found = False
            for v in st.session_state.usage_violations:
                if v['user_id'] == search_user or v['name'].lower() == search_user.lower():
                    st.session_state.usage_violations = [
                        viol for viol in st.session_state.usage_violations 
                        if viol['user_id'] != v['user_id']
                    ]
                    st.success(f"Removed user: {v['name']}")
                    found = True
                    st.rerun()
                    break
            if not found:
                st.warning("User not found in violations list")
        else:
            st.warning("Please enter a name or User ID to search")