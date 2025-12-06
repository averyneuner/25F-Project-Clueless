import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import altair as alt

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
SideBarLinks()


API_BASE_URL = "http://web-api:4000"


def get_admin_users():
    """GET /admin/users"""
    try:
        resp = requests.get(f"{API_BASE_URL}/admin/users", timeout=10)
        return (True, resp.json()) if resp.status_code == 200 else (False, resp.text)
    except Exception as e:
        return False, str(e)

def get_admin_logs():
    """GET /admin/logs"""
    try:
        resp = requests.get(f"{API_BASE_URL}/admin/logs", timeout=10)
        return (True, resp.json()) if resp.status_code == 200 else (False, resp.text)
    except Exception as e:
        return False, str(e)


success_users, users_data = get_admin_users()
success_logs, logs_data = get_admin_logs()


st.title("Dashboard & Overview Page")


col1, col2, col3 = st.columns(3)
with col1:
    total_users = len(users_data) if success_users else 0
    st.metric("👥 Total Users", total_users)
with col2:
    biz_logs = len(logs_data.get('business_logs', [])) if success_logs else 0
    st.metric("🏢 Business Logs", biz_logs)
with col3:
    tech_logs = len(logs_data.get('tech_logs', [])) if success_logs else 0
    st.metric("👨‍💻 Tech Logs", tech_logs)

st.divider()


st.subheader("👥 User Management")
if success_users and users_data:
    df = pd.DataFrame(users_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("📥 Export CSV", df.to_csv(index=False), "users.csv", "text/csv")
else:
    st.error(f"Failed to load users: {users_data}")

st.divider()


st.subheader("📋 System Logs")
if success_logs:
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🏢 Business Logs**")
        biz_logs_list = logs_data.get('business_logs', [])
        if biz_logs_list:
            for i, log in enumerate(biz_logs_list):
                status = log.get('BusinessStatus', 'Unknown')
                icon = "🟢" if status == "Read" else "🔴"
                with st.expander(f"{icon} Log {i+1} - {status}"):
                    st.write(f"**Issues:** {log.get('Issues', 'None')}")
        else:
            st.info("No business logs")
    
    with col2:
        st.write("**👨‍💻 Tech Logs**")
        tech_logs_list = logs_data.get('tech_logs', [])
        if tech_logs_list:
            for log in tech_logs_list:
                with st.expander(f"🔧 {log.get('Name', 'Unknown')}"):
                    st.write(f"**System ID:** {log.get('SystemID')}")
                    st.write(f"**Issues:** {log.get('IssueLogs', 'None')}")
        else:
            st.info("No tech logs")
else:
    st.warning(f"Could not load logs: {logs_data}")

st.divider()
st.caption("💡 Data refreshes on page load.")


st.divider()

st.subheader("Business Client Management")

if st.button("Business Client Management", use_container_width=True, type="primary"):
    st.switch_page("pages/23_Business_Client_Mgmt.py")
