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
    """GET /customer/customer/<int:customer_id>/notifications"""
    try:
        resp = requests.get(f"{API_BASE_URL}/customer/customer/{customer_id}/notifications", timeout=10)
        return (True, resp.json()) if resp.status_code == 200 else (False, resp.text)
    except Exception as e:
        return False, str(e)

def send_customer_notification(customer_id, message):
    """POST /customer/customer/<int:customer_id>/notifications"""
    try:
        resp = requests.post(
            f"{API_BASE_URL}/customer/customer/{customer_id}/notifications",
            json={"message": message, "status": "Unread"}, timeout=10
        )
        return (True, resp.json()) if resp.status_code in [200, 201] else (False, resp.text)
    except Exception as e:
        return False, str(e)

def get_business_notifications(business_id):
    """GET /business/business/<int:business_id>/notifications"""
    try:
        resp = requests.get(f"{API_BASE_URL}/business/business/{business_id}/notifications", timeout=10)
        return (True, resp.json()) if resp.status_code == 200 else (False, resp.text)
    except Exception as e:
        return False, str(e)

def send_business_notification(business_id, message):
    """POST /business/business/<int:business_id>/notifications"""
    try:
        resp = requests.post(
            f"{API_BASE_URL}/business/business/{business_id}/notifications",
            json={"message": message, "status": "Unread"}, timeout=10
        )
        return (True, resp.json()) if resp.status_code in [200, 201] else (False, resp.text)
    except Exception as e:
        return False, str(e)

def delete_business_notification(business_id, notif_id):
    """DELETE /business/business/<int:business_id>/notifications/<int:notification_id>"""
    try:
        resp = requests.delete(f"{API_BASE_URL}/business/business/{business_id}/notifications/{notif_id}", timeout=10)
        return (True, resp.json()) if resp.status_code == 200 else (False, resp.text)
    except Exception as e:
        return False, str(e)

def get_admin_users():
    """GET /general/admin/users - for dropdown"""
    try:
        resp = requests.get(f"{API_BASE_URL}/general/admin/users", timeout=10)
        return (True, resp.json()) if resp.status_code == 200 else (False, [])
    except:
        return False, []


customer_id = 10
business_id = 10
success_cust, cust_notifs = get_customer_notifications(customer_id)
success_biz, biz_notifs = get_business_notifications(business_id)
_, users_data = get_admin_users()


st.title("Notifications & Alerts Page")



col1, col2 = st.columns(2)
with col1:
    unread_cust = sum(1 for n in (cust_notifs or []) if n.get('Status') == 'Unread') if success_cust else 0
    st.metric("👤 Customer Unread", unread_cust)
with col2:
    unread_biz = sum(1 for n in (biz_notifs or []) if n.get('Status') == 'Unread') if success_biz else 0
    st.metric("🏢 Business Unread", unread_biz)

st.divider()


st.subheader("📤 Send Notification")

notif_type = st.radio("Send to:", ["👤 Customer", "🏢 Business"], horizontal=True)

col1, col2 = st.columns([1, 2])
with col1:
    if "Customer" in notif_type:
        if users_data:
            options = {f"{u['FirstName']} {u['LastName']}": u['CustomerID'] for u in users_data}
            selected = st.selectbox("Recipient", list(options.keys()))
            recipient_id = options[selected]
        else:
            recipient_id = st.number_input("Customer ID", min_value=1, value=customer_id, key="send_cust")
    else:
        recipient_id = st.number_input("Business ID", min_value=1, value=business_id, key="send_biz")

with col2:
    message = st.text_area("Message", placeholder="Type message...", height=100)

if st.button("📨 Send", type="primary", disabled=not message.strip()):
    if "Customer" in notif_type:
        success, result = send_customer_notification(recipient_id, message.strip())
    else:
        success, result = send_business_notification(recipient_id, message.strip())
    
    if success:
        st.success(f"✅ Sent! ID: {result.get('NotificationID', 'N/A')}")
        st.rerun()
    else:
        st.error(f"❌ Failed: {result}")

st.divider()


st.subheader("📋 View Notifications")

tab1, tab2 = st.tabs(["👤 Customer", "🏢 Business"])

with tab1:
    if success_cust and cust_notifs:
        for notif in cust_notifs:
            status = notif.get('Status', 'Unknown')
            icon = "🔴" if status == "Unread" else "⚪"
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{icon} **#{notif.get('NotificationID')}** - {status}")
                    st.caption(notif.get('Message', 'No message')[:100])
                with col2:
                    st.caption(f"Customer: {notif.get('CustomerID')}")
    else:
        st.info("No customer notifications")

with tab2:
    if success_biz and biz_notifs:
        for notif in biz_notifs:
            status = notif.get('Status', 'Unknown')
            icon = "🔴" if status == "Unread" else "⚪"
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{icon} **{notif.get('CompanyName', 'Unknown')}**")
                    st.caption(notif.get('Message', 'No message')[:100])
                with col2:
                    if st.button("🗑️", key=f"del_{notif['NotificationID']}"):
                        success, _ = delete_business_notification(business_id, notif['NotificationID'])
                        if success:
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("No business notifications")

st.divider()
st.caption("💡 Data refreshes on page load.")