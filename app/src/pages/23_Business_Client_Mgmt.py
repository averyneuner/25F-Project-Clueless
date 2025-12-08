import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests


st.set_page_config(layout='wide')
SideBarLinks()


API_BASE_URL = "http://web-api:4000"


st.title('Business Client Management Page')

def get_all_business():
    """GET /business/users"""
    try:
        resp = requests.get(f"{API_BASE_URL}/business/users", timeout=10)
        return (True, resp.json()) if resp.status_code == 200 else (False, [])
    except:
        return False, []

def create_business(data):
    """POST /business/users"""
    try:
        resp = requests.post(f"{API_BASE_URL}/business/users", json=data, timeout=10)
        return (True, resp.json()) if resp.status_code == 201 else (False, resp.text)
    except Exception as e:
        return False, str(e)

def delete_business(company_id):
    """DELETE /business/users/<int:company_id>"""
    try:
        resp = requests.delete(f"{API_BASE_URL}/business/users/{company_id}", timeout=10)
        return (True, resp.json()) if resp.status_code == 200 else (False, resp.text)
    except Exception as e:
        return False, str(e)


if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'list'
if 'selected_client' not in st.session_state:
    st.session_state.selected_client = None


success, businesses = get_all_business()


if st.session_state.view_mode != 'list':
    if st.button("Back"):
        st.session_state.view_mode = 'list'
        st.session_state.selected_client = None
        st.rerun()


if st.session_state.view_mode == 'list':
    
    col1, col2 = st.columns([4, 1])
    with col1:
        search = st.text_input("Search", placeholder="Search by company name", label_visibility="collapsed")
    with col2:
        if st.button("Add", use_container_width=True, type="primary"):
            st.session_state.view_mode = 'add'
            st.rerun()
    
    st.divider()
    st.subheader(f"Business Clients ({len(businesses) if success else 0})")
    
    if success and businesses:
        for client in businesses:
            if search and search.lower() not in client.get('CompanyName', '').lower():
                continue
            
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{client.get('CompanyName', 'N/A')}**")
                    st.caption(f"ID: {client.get('CompanyID')} | {client.get('ContactEmail', 'N/A')}")
                    st.caption(f"{client.get('City', '')}, {client.get('State', '')} {client.get('Country', '')}")
                with col2:
                    if st.button("View", key=f"view_{client['CompanyID']}", use_container_width=True):
                        st.session_state.selected_client = client
                        st.session_state.view_mode = 'profile'
                        st.rerun()
    else:
        st.warning("No businesses found or API unavailable")

elif st.session_state.view_mode == 'profile':
    st.title('Business Client Profile')
    
    client = st.session_state.selected_client
    if client:
        st.subheader(client.get('CompanyName', 'Unknown'))
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Company ID**")
            st.write(client.get('CompanyID', 'N/A'))
            st.write("**Contact Email**")
            st.write(client.get('ContactEmail', 'N/A'))
            st.write("**Popularity**")
            st.write(f"{client.get('PopularityPercentage', 0)}%")
        with col2:
            st.write("**Address**")
            st.write(client.get('StreetAddress', 'N/A'))
            st.write(f"{client.get('City', '')}, {client.get('State', '')} {client.get('ZIP', '')}")
            st.write(client.get('Country', 'N/A'))
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Remove", use_container_width=True):
                success, result = delete_business(client['CompanyID'])
                if success:
                    st.success(f"Removed {client['CompanyName']}!")
                    st.session_state.view_mode = 'list'
                    st.session_state.selected_client = None
                    st.rerun()
                else:
                    st.error(f"Failed: {result}")
        with col2:
            if st.button("Next", use_container_width=True, type="primary"):
                if businesses:
                    ids = [b['CompanyID'] for b in businesses]
                    curr_idx = ids.index(client['CompanyID']) if client['CompanyID'] in ids else 0
                    next_idx = (curr_idx + 1) % len(businesses)
                    st.session_state.selected_client = businesses[next_idx]
                    st.rerun()


elif st.session_state.view_mode == 'add':
    st.title('Add Business Client')
    
    with st.form("add_business_form"):
        st.write("**Company Name** *")
        company_name = st.text_input("Name", placeholder="Enter company name", label_visibility="collapsed")
        
        st.write("**Contact Email** *")
        contact_email = st.text_input("Email", placeholder="contact@company.com", label_visibility="collapsed")
        
        st.write("**Address**")
        col1, col2 = st.columns(2)
        with col1:
            street = st.text_input("Street", placeholder="Street Address", label_visibility="collapsed")
            city = st.text_input("City", placeholder="City", label_visibility="collapsed")
        with col2:
            state = st.text_input("State", placeholder="State", label_visibility="collapsed")
            zip_code = st.text_input("ZIP", placeholder="ZIP Code", label_visibility="collapsed")
        
        country = st.selectbox("Country", ["USA", "Canada", "UK", "France", "Germany", "Italy", "Japan", "Other"])
        
        submitted = st.form_submit_button("Add Business", type="primary", use_container_width=True)
        
        if submitted:
            if not company_name or not contact_email:
                st.error("⚠️ Company Name and Email are required")
            else:
                data = {
                    "company_name": company_name,
                    "contact_email": contact_email,
                    "street": street,
                    "city": city,
                    "state": state,
                    "zip": zip_code,
                    "country": country
                }
                success, result = create_business(data)
                if success:
                    st.success(f"✅ {company_name} added! ID: {result.get('CompanyID')}")
                    st.session_state.view_mode = 'list'
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {result}")