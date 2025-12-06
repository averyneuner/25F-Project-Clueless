import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
SideBarLinks()


API_BASE_URL = "http://web-api:4000"

def get_customer_notifications(customer_id):
    """
    Calls: GET /c/customer/<customer_id>/notifications
    Backend route: @customer.route("/customer/<int:customer_id>/notifications", methods=["GET"])
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}/c/customer/{customer_id}/notifications",
            timeout=10
        )
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}: {response.text}"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to API server"
    except requests.exceptions.RequestException as e:
        return False, str(e)


def get_business_notifications(business_id):
    """
    Calls: GET /b/business/<business_id>/notifications
    Backend route: @business.route("/business/<int:business_id>/notifications", methods=["GET"])
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}/b/business/{business_id}/notifications",
            timeout=10
        )
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return False, str(e)


def send_customer_notification(customer_id, message):
    """
    Calls: POST /c/customer/<customer_id>/notifications
    Backend route: @customer.route("/customer/<int:customer_id>/notifications", methods=["POST"])
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/c/customer/{customer_id}/notifications",
            json={
                "message": message,
                "status": "Unread"
            },
            timeout=10
        )
        if response.status_code in [200, 201]:
            return True, response.json()
        return False, f"HTTP {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return False, str(e)


def send_business_notification(business_id, message):
    """
    Calls: POST /b/business/<business_id>/notifications
    Backend route: @business.route("/business/<int:business_id>/notifications", methods=["POST"])
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/b/business/{business_id}/notifications",
            json={
                "message": message,
                "status": "Unread"
            },
            timeout=10
        )
        if response.status_code in [200, 201]:
            return True, response.json()
        return False, f"HTTP {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return False, str(e)


def delete_business_notification(business_id, notification_id):
    """
    Calls: DELETE /b/business/<business_id>/notifications/<notification_id>
    Backend route: @business.route("/business/<int:business_id>/notifications/<int:notification_id>", methods=["DELETE"])
    """
    try:
        response = requests.delete(
            f"{API_BASE_URL}/b/business/{business_id}/notifications/{notification_id}",
            timeout=10
        )
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return False, str(e)


def get_admin_users():
    """
    Calls: GET /g/admin/users
    Used to populate receiver dropdown with customer list
    """
    try:
        response = requests.get(f"{API_BASE_URL}/g/admin/users", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)




if 'notif_view' not in st.session_state:
    st.session_state.notif_view = 'landing'

if 'selected_notif' not in st.session_state:
    st.session_state.selected_notif = None

if 'selected_customer_id' not in st.session_state:
    st.session_state.selected_customer_id = 10

if 'selected_business_id' not in st.session_state:
    st.session_state.selected_business_id = 10



def count_unread(notifications):
    """Count unread notifications from a list"""
    if not notifications:
        return 0
    return sum(1 for n in notifications if n.get('Status') == 'Unread')

def back_button(target='landing'):
    """Render a back button that changes view state"""
    if st.button("← Back"):
        st.session_state.notif_view = target
        st.session_state.selected_notif = None
        st.rerun()


success_users, users_data = get_admin_users()


success_cust_notif, customer_notifications = get_customer_notifications(
    st.session_state.selected_customer_id
)


success_biz_notif, business_notifications = get_business_notifications(
    st.session_state.selected_business_id
)


if st.session_state.notif_view == 'landing':
    st.title('🔔 Notifications & Alerts Page')
    
    with st.sidebar:
        st.subheader("🔌 API Status")
        if success_cust_notif:
            st.success("✅ Connected")
        else:
            st.error("❌ Disconnected")
        
        st.divider()
        
        st.subheader("👤 Select Customer")
        if success_users and users_data:
            customer_options = {
                f"{u['FirstName']} {u['LastName']} (ID: {u['CustomerID']})": u['CustomerID']
                for u in users_data
            }
            selected = st.selectbox(
                "Customer",
                options=list(customer_options.keys()),
                label_visibility="collapsed"
            )
            st.session_state.selected_customer_id = customer_options[selected]
        else:
            st.session_state.selected_customer_id = st.number_input(
                "Customer ID", 
                min_value=1, 
                value=10
            )
        
        st.subheader("🏢 Select Business")
        st.session_state.selected_business_id = st.number_input(
            "Business ID",
            min_value=1,
            value=10,
            label_visibility="collapsed"
        )
    

    st.markdown("### ⚠️ Alerts Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cust_unread = count_unread(customer_notifications) if success_cust_notif else 0
        st.metric("Customer Notifications", cust_unread, help="Unread customer notifications")
    
    with col2:
        biz_unread = count_unread(business_notifications) if success_biz_notif else 0
        st.metric("Business Notifications", biz_unread, help="Unread business notifications")
    
    with col3:
        total_unread = cust_unread + biz_unread
        st.metric("Total Unread", total_unread)
    
    st.write("")
    

    if st.button("🔔 View All Notifications & Alerts →", use_container_width=True, type="primary"):
        st.session_state.notif_view = 'view'
        st.rerun()
    
    st.divider()
    

    st.subheader('📤 Send New Notification')
    

    notif_type = st.radio(
        "Send to:",
        ["Customer", "Business"],
        horizontal=True
    )
    

    st.write("**Receiver**")
    if notif_type == "Customer":
        if success_users and users_data:
            receiver_options = {
                f"{u['FirstName']} {u['LastName']} ({u['EmailAddress']})": u['CustomerID']
                for u in users_data
            }
            selected_receiver = st.selectbox(
                "Select Customer",
                options=list(receiver_options.keys()),
                label_visibility="collapsed"
            )
            receiver_id = receiver_options[selected_receiver]
        else:
            receiver_id = st.number_input("Customer ID", min_value=1, value=10, label_visibility="collapsed")
    else:
        receiver_id = st.number_input("Business ID", min_value=1, value=10, label_visibility="collapsed")
    

    st.write("**Message**")
    message = st.text_area(
        "Message",
        placeholder="Type your notification message here...",
        max_chars=200,
        label_visibility="collapsed",
        height=150
    )
    st.caption(f"{len(message)}/200 characters")
    
    st.write("")
    

    send_disabled = not message or len(message.strip()) == 0
    
    if st.button("📨 Send Notification", use_container_width=True, type="primary", disabled=send_disabled):
        if notif_type == "Customer":
            success, result = send_customer_notification(receiver_id, message)
        else:
            success, result = send_business_notification(receiver_id, message)
        
        if success:
            st.success(f"✅ Notification sent successfully! ID: {result.get('NotificationID', 'N/A')}")
            st.balloons()
            st.rerun()
        else:
            st.error(f"❌ Failed to send: {result}")


elif st.session_state.notif_view == 'view':
    back_button('landing')
    st.title('📋 View Notifications & Alerts')
    

    tab1, tab2 = st.tabs(["👤 Customer Notifications", "🏢 Business Notifications"])
    

    with tab1:
        if success_cust_notif and customer_notifications:
            # Separate unread and read
            unread = [n for n in customer_notifications if n.get('Status') == 'Unread']
            read = [n for n in customer_notifications if n.get('Status') != 'Unread']
            
            # Unread Section
            st.subheader(f"🔴 Unread ({len(unread)})")
            
            if unread:
                for notif in unread:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([0.5, 8, 2])
                        with col1:
                            st.markdown("🔴")
                        with col2:
                            st.markdown(f"**Notification #{notif.get('NotificationID', 'N/A')}**")
                            st.write(notif.get('Message', 'No message'))
                        with col3:
                            if st.button("View →", key=f"view_cust_{notif['NotificationID']}", use_container_width=True):
                                st.session_state.selected_notif = {
                                    **notif,
                                    'type': 'customer',
                                    'timestamp': datetime.now()
                                }
                                st.session_state.notif_view = 'detail'
                                st.rerun()
            else:
                st.info("🎉 No unread notifications!")
            
            st.divider()
            
            # Read Section
            st.subheader(f"✅ Read ({len(read)})")
            
            if read:
                for notif in read:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([0.5, 8, 2])
                        with col1:
                            st.markdown("⚪")
                        with col2:
                            st.markdown(f"**Notification #{notif.get('NotificationID', 'N/A')}**")
                            st.write(notif.get('Message', 'No message'))
                        with col3:
                            if st.button("View →", key=f"view_cust_read_{notif['NotificationID']}", use_container_width=True):
                                st.session_state.selected_notif = {
                                    **notif,
                                    'type': 'customer',
                                    'timestamp': datetime.now()
                                }
                                st.session_state.notif_view = 'detail'
                                st.rerun()
            else:
                st.info("No read notifications")
        else:
            st.warning(f"Could not load customer notifications: {customer_notifications}")
    

    with tab2:
        if success_biz_notif and business_notifications:
            # Separate unread and read
            unread = [n for n in business_notifications if n.get('Status') == 'Unread']
            read = [n for n in business_notifications if n.get('Status') != 'Unread']
            
            # Unread Section
            st.subheader(f"🔴 Unread ({len(unread)})")
            
            if unread:
                for notif in unread:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([0.5, 8, 2])
                        with col1:
                            st.markdown("🔴")
                        with col2:
                            st.markdown(f"**{notif.get('CompanyName', 'Unknown Company')}**")
                            st.write(notif.get('Message', 'No message'))
                        with col3:
                            if st.button("View →", key=f"view_biz_{notif['NotificationID']}", use_container_width=True):
                                st.session_state.selected_notif = {
                                    **notif,
                                    'type': 'business',
                                    'timestamp': datetime.now()
                                }
                                st.session_state.notif_view = 'detail'
                                st.rerun()
            else:
                st.info("🎉 No unread business notifications!")
            
            st.divider()
            
            # Read Section
            st.subheader(f"✅ Read ({len(read)})")
            
            if read:
                for notif in read:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([0.5, 8, 2])
                        with col1:
                            st.markdown("⚪")
                        with col2:
                            st.markdown(f"**{notif.get('CompanyName', 'Unknown Company')}**")
                            st.write(notif.get('Message', 'No message'))
                        with col3:
                            if st.button("View →", key=f"view_biz_read_{notif['NotificationID']}", use_container_width=True):
                                st.session_state.selected_notif = {
                                    **notif,
                                    'type': 'business',
                                    'timestamp': datetime.now()
                                }
                                st.session_state.notif_view = 'detail'
                                st.rerun()
            else:
                st.info("No read business notifications")
        else:
            st.warning(f"Could not load business notifications: {business_notifications}")


elif st.session_state.notif_view == 'detail':
    back_button('view')
    
    notif = st.session_state.selected_notif
    
    if notif:
        notif_type = notif.get('type', 'customer')
        type_icon = "👤" if notif_type == 'customer' else "🏢"
        st.title(f"{type_icon} Notification Details")
        

        with st.container(border=True):
            st.markdown(f"**Notification ID:** #{notif.get('NotificationID', 'N/A')}")
            st.markdown(f"**Status:** {notif.get('Status', 'Unknown')}")
            
            if notif_type == 'business':
                st.markdown(f"**Company:** {notif.get('CompanyName', 'N/A')}")
                st.markdown(f"**Contact:** {notif.get('ContactEmail', 'N/A')}")
            else:
                st.markdown(f"**Customer ID:** {notif.get('CustomerID', 'N/A')}")
            
            timestamp = notif.get('timestamp', datetime.now())
            st.caption(f"Viewed: {timestamp.strftime('%B %d, %Y at %I:%M %p')}")
        
        st.divider()
        

        st.subheader("📝 Message")
        st.write(notif.get('Message', 'No message content'))
        
        st.divider()
        

        st.subheader("⚡ Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_status = notif.get('Status', 'Unread')
            if current_status == 'Read':
                btn_label = "🔴 Mark as Unread"
                new_status = "Unread"
            else:
                btn_label = "✅ Mark as Read"
                new_status = "Read"
            
            if st.button(btn_label, use_container_width=True, type="primary"):

                st.success(f"Marked as {new_status}!")
                st.session_state.notif_view = 'view'
                st.rerun()
        
        with col2:
            if st.button("🗑️ Delete Notification", use_container_width=True):
                if notif_type == 'business':
                    company_id = notif.get('CompanyID', st.session_state.selected_business_id)
                    success, result = delete_business_notification(
                        company_id,
                        notif['NotificationID']
                    )
                    if success:
                        st.success("✅ Notification deleted!")
                        st.session_state.notif_view = 'view'
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to delete: {result}")
                else:
                    st.warning("⚠️ Customer notification deletion not implemented in backend")
    else:
        st.error("❌ Notification not found")
        if st.button("← Back to List"):
            st.session_state.notif_view = 'view'
            st.rerun()

st.divider()
st.caption("💡 Select a customer/business in the sidebar to view their notifications.")