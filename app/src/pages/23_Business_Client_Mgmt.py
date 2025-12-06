import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE_URL = "http://web-api:4000"


if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'list'

if 'selected_client' not in st.session_state:
    st.session_state.selected_client = None

if st.session_state.selected_client is not None:
    if 'company_id' not in st.session_state.selected_client:
        st.session_state.selected_client = None
        st.session_state.view_mode = 'list'

if 'business_clients' in st.session_state:
    if st.session_state.business_clients and 'company_id' not in st.session_state.business_clients[0]:
        del st.session_state['business_clients']


if 'business_clients' not in st.session_state:
    st.session_state.business_clients = [
        {
            'company_id': 10,
            'company_name': 'Gucci',
            'business_type': 'Luxury Fashion',
            'contact_name': 'Adam Smith',
            'street': '195 Broadway',
            'city': 'New York',
            'state': 'NY',
            'zip': '10007',
            'country': 'USA'
        },
        {
            'company_id': 11,
            'company_name': 'Gap',
            'business_type': 'Retail',
            'contact_name': 'Jane Doe',
            'street': '2 Folsom St',
            'city': 'San Francisco',
            'state': 'CA',
            'zip': '94105',
            'country': 'USA'
        },
        {
            'company_id': 12,
            'company_name': 'Target Style',
            'business_type': 'Fast Fashion',
            'contact_name': 'John Wilson',
            'street': '1000 Nicollet Mall',
            'city': 'Minneapolis',
            'state': 'MN',
            'zip': '55403',
            'country': 'USA'
        }
    ]


if st.session_state.view_mode != 'list':
    if st.button("← Back"):
        st.session_state.view_mode = 'list'
        st.session_state.selected_client = None
        st.rerun()


if st.session_state.view_mode == 'list':
    st.title('Business Client Management')
    
    col1, col2 = st.columns([5, 1])
    with col1:
        search = st.text_input("Search", placeholder="🔍 Search", label_visibility="collapsed")
    with col2:
        st.button("⚙️ Filter")
    
    st.divider()
    
    st.subheader("Business Client")
    
    for client in st.session_state.business_clients:
        if 'company_id' not in client:
            continue
            
        if search and search.lower() not in client.get('company_name', '').lower():
            continue
            
        with st.container():
            st.write("**Company ID**")
            st.write(client.get('company_id', 'N/A'))
            
            st.write("**Company Name**")
            st.write(client.get('company_name', 'N/A'))
            
            st.write("**Business Type**")
            st.write(client.get('business_type', 'N/A'))
            
            st.write("**Contact Name**")
            st.write(client.get('contact_name', 'N/A'))
            
            if st.button(f"Business Client Profile →", key=f"profile_{client.get('company_id')}", use_container_width=True):
                st.session_state.selected_client = client
                st.session_state.view_mode = 'profile'
                st.rerun()
            
            st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Edit", use_container_width=True):
            st.info("Select a client profile first to edit")
    with col2:
        if st.button("Add", use_container_width=True, type="primary"):
            st.session_state.view_mode = 'add'
            st.rerun()

elif st.session_state.view_mode == 'profile':
    st.title('Business Client Profile')
    
    col1, col2 = st.columns([5, 1])
    with col1:
        st.text_input("Search", placeholder="🔍 Search", label_visibility="collapsed", key="profile_search")
    with col2:
        st.button("⚙️", key="profile_filter")
    
    st.divider()
    
    client = st.session_state.selected_client
    
    if client and 'company_id' in client:
        st.subheader("Profile")
        
        st.write("**Company ID**")
        st.write(client.get('company_id', 'N/A'))
        
        st.write("**Company Name**")
        st.write(client.get('company_name', 'N/A'))
        
        st.write("**Business Type**")
        st.write(client.get('business_type', 'N/A'))
        
        st.write("**Contact Name**")
        st.write(client.get('contact_name', 'N/A'))
        
        st.write("**Address**")
        address = f"{client.get('zip', '')}, {client.get('street', '')}, {client.get('city', '')}, {client.get('state', '')}, {client.get('country', '')}"
        st.write(address)
        
        st.divider()
        
        st.button("View uploaded document →", use_container_width=True, disabled=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Remove", use_container_width=True):
                st.session_state.business_clients = [
                    c for c in st.session_state.business_clients 
                    if c.get('company_id') != client.get('company_id')
                ]
                st.session_state.view_mode = 'list'
                st.session_state.selected_client = None
                st.success(f"{client.get('company_name', 'Client')} removed!")
                st.rerun()
        with col2:
            if st.button("Next", use_container_width=True, type="primary"):
                current_idx = next((i for i, c in enumerate(st.session_state.business_clients) 
                                   if c.get('company_id') == client.get('company_id')), 0)
                next_idx = (current_idx + 1) % len(st.session_state.business_clients)
                st.session_state.selected_client = st.session_state.business_clients[next_idx]
                st.rerun()
    else:
        st.warning("Client data not found. Returning to list...")
        st.session_state.view_mode = 'list'
        st.session_state.selected_client = None
        st.rerun()


elif st.session_state.view_mode == 'add':
    st.title('Add Business Client')
    
    st.subheader("Business Profile")
    
    with st.form("add_client_form"):
        # 1. Company ID
        st.write("**Company ID**")
        company_id = st.number_input(
            "Company ID", 
            min_value=1, 
            value=1, 
            label_visibility="collapsed",
            help="Unique identifier for the company"
        )
        
        # 2. Company Name
        st.write("**Company Name**")
        company_name = st.text_input(
            "Company Name", 
            placeholder="Please enter company name", 
            label_visibility="collapsed"
        )
        
        # 3. Business Type
        st.write("**Business Type**")
        business_type = st.selectbox(
            "Business Type",
            [
                "---- Please select the option ----", 
                "Fast Fashion", 
                "Luxury Fashion", 
                "Retail", 
                "Sustainable Fashion",
                "Streetwear",
                "Athletic Wear",
                "E-commerce"
            ],
            label_visibility="collapsed"
        )
        
        # 4. Contact Name
        st.write("**Contact Name**")
        contact_name = st.text_input(
            "Contact Name", 
            placeholder="Please enter contact name", 
            label_visibility="collapsed"
        )
        
        # 5. Address Section
        st.write("**Address**")
        
        col1, col2 = st.columns(2)
        with col1:
            zip_code = st.text_input("ZIP", placeholder="ZIP Code", label_visibility="collapsed")
        with col2:
            street = st.text_input("Street", placeholder="Street Address", label_visibility="collapsed")
        
        col1, col2 = st.columns(2)
        with col1:
            city = st.text_input("City", placeholder="City", label_visibility="collapsed")
        with col2:
            state = st.text_input("State", placeholder="State", label_visibility="collapsed")
        
        country = st.selectbox(
            "Country",
            ["---- Please select the option ----", "USA", "Canada", "UK", "France", "Germany", "Italy", "Japan", "Other"],
            label_visibility="collapsed"
        )
        
        st.write("")
        
        # Submit Button
        submitted = st.form_submit_button("Add", use_container_width=True, type="primary")
        
        if submitted:
            # Validation
            if not company_name:
                st.error("Please enter Company Name")
            elif business_type == "---- Please select the option ----":
                st.error("Please select Business Type")
            elif not contact_name:
                st.error("Please enter Contact Name")
            elif country == "---- Please select the option ----":
                st.error("Please select Country")
            else:
                # Check if company_id already exists
                existing_ids = [c.get('company_id') for c in st.session_state.business_clients if 'company_id' in c]
                if company_id in existing_ids:
                    st.error(f"Company ID {company_id} already exists. Please use a different ID.")
                else:
                    new_client = {
                        'company_id': company_id,
                        'company_name': company_name,
                        'business_type': business_type,
                        'contact_name': contact_name,
                        'zip': zip_code or 'N/A',
                        'street': street or 'N/A',
                        'city': city or 'N/A',
                        'state': state or 'N/A',
                        'country': country
                    }
                    st.session_state.business_clients.append(new_client)
                    st.success(f"{company_name} has been successfully added!")
                    st.session_state.view_mode = 'list'
                    st.rerun()