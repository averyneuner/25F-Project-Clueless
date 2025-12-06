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
    """
    Calls: GET /g/admin/users
    Backend route: @general.route("/admin/users", methods=["GET"])
    """
    try:
        response = requests.get(f"{API_BASE_URL}/g/admin/users", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}: {response.text}"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to API server. Is the backend running?"
    except requests.exceptions.Timeout:
        return False, "Request timed out"
    except requests.exceptions.RequestException as e:
        return False, str(e)


def get_admin_logs():
    """
    Calls: GET /g/admin/logs
    Backend route: @general.route("/admin/logs", methods=["GET"])
    Returns: {"business_logs": [...], "tech_logs": [...]}
    """
    try:
        response = requests.get(f"{API_BASE_URL}/g/admin/logs", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)


def get_trends():
    """
    Calls: GET /a/analytics/trend
    Backend route: @analytics.route("/analytics/trend", methods=["GET"])
    """
    try:
        response = requests.get(f"{API_BASE_URL}/a/analytics/trend", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)


def get_demand():
    """
    Calls: GET /a/analytics/demand
    Backend route: @analytics.route("/analytics/demand", methods=["GET"])
    """
    try:
        response = requests.get(f"{API_BASE_URL}/a/analytics/demand", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)




success_users, users_data = get_admin_users()
success_logs, logs_data = get_admin_logs()
success_trends, trends_data = get_trends()
success_demand, demand_data = get_demand()



st.title('📊 Dashboard & Overview Page')


with st.sidebar:
    st.subheader("🔌 API Status")
    if success_users:
        st.success("✅ Backend Connected")
    else:
        st.error("❌ Connection Failed")
        st.caption(f"Error: {users_data}")
    
    st.divider()
    st.caption(f"API URL: {API_BASE_URL}")


st.subheader('Top KPIs')

col1, col2, col3 = st.columns(3)

with col1:
    total_users = len(users_data) if success_users and isinstance(users_data, list) else 0
    st.metric(label="👥 Total Users", value=f"{total_users:,}")

with col2:
    business_count = 96
    if success_logs:
        business_logs = logs_data.get('business_logs', [])
        if business_logs:
            business_count = len(business_logs)
    st.metric(label="🏢 Total Business Clients", value=business_count)

with col3:
    pending = 0
    if success_logs:
        pending = len(logs_data.get('business_logs', []))
    st.metric(label="⏳ Pending Approvals", value=pending, help="Users / Retailers awaiting approval")

st.divider()


st.subheader('📈 Weekly New Signups')
st.caption("Users / Businesses / Daily Outfits Uploads / Wishlist Conversions")


if 'show_charts' not in st.session_state:
    st.session_state['show_charts'] = False


if st.button("📊 Graphs / Charts ↓", use_container_width=True):
    st.session_state['show_charts'] = not st.session_state['show_charts']

if st.session_state.get('show_charts', False):
    days = ["Su", "M", "T", "W", "Th", "F", "S"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**👥 Users**")
        users_df = pd.DataFrame({
            "Day": days,
            "Count": [550, 625, 475, 600, 350, 750, 675]
        })
        chart = alt.Chart(users_df).mark_bar(color="#A78BFA").encode(
            x=alt.X("Day:N", sort=days, title="Day"),
            y=alt.Y("Count:Q", scale=alt.Scale(domain=[0, 800]), title="Signups")
        ).properties(height=200)
        st.altair_chart(chart, use_container_width=True)
        
        st.write("**👗 Daily Outfit Uploads**")
        uploads_df = pd.DataFrame({
            "Day": days,
            "Count": [220, 150, 190, 160, 80, 200, 325]
        })
        chart = alt.Chart(uploads_df).mark_bar(color="#A78BFA").encode(
            x=alt.X("Day:N", sort=days, title="Day"),
            y=alt.Y("Count:Q", scale=alt.Scale(domain=[0, 700]), title="Uploads")
        ).properties(height=200)
        st.altair_chart(chart, use_container_width=True)
    
    with col2:
        st.write("**🏢 Businesses**")
        biz_df = pd.DataFrame({
            "Day": days,
            "Count": [300, 450, 400, 500, 250, 600, 550]
        })
        chart = alt.Chart(biz_df).mark_bar(color="#A78BFA").encode(
            x=alt.X("Day:N", sort=days, title="Day"),
            y=alt.Y("Count:Q", scale=alt.Scale(domain=[0, 800]), title="Signups")
        ).properties(height=200)
        st.altair_chart(chart, use_container_width=True)
        
        st.write("**💝 Wishlist Conversions**")
        wishlist_df = pd.DataFrame({
            "Day": days,
            "Count": [400, 250, 335, 420, 550, 600, 750]
        })
        chart = alt.Chart(wishlist_df).mark_bar(color="#A78BFA").encode(
            x=alt.X("Day:N", sort=days, title="Day"),
            y=alt.Y("Count:Q", scale=alt.Scale(domain=[0, 800]), title="Conversions")
        ).properties(height=200)
        st.altair_chart(chart, use_container_width=True)

st.divider()


st.subheader('👥 User Management')

if success_users and users_data:
    df_users = pd.DataFrame(users_data)
    
    st.dataframe(
        df_users,
        use_container_width=True,
        hide_index=True,
        column_config={
            "CustomerID": st.column_config.NumberColumn("ID", width="small"),
            "FirstName": st.column_config.TextColumn("First Name"),
            "LastName": st.column_config.TextColumn("Last Name"),
            "EmailAddress": st.column_config.TextColumn("Email"),
            "TotalClosets": st.column_config.NumberColumn("Closets", width="small")
        }
    )
    
    csv = df_users.to_csv(index=False)
    st.download_button(
        label="📥 Export Users to CSV",
        data=csv,
        file_name="users_export.csv",
        mime="text/csv"
    )
else:
    st.error(f"❌ Failed to load users: {users_data}")
    st.info("💡 Make sure the Flask backend is running on port 4000")

st.divider()


st.subheader('📋 System Logs')

if success_logs:
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🏢 Business Logs**")
        business_logs = logs_data.get('business_logs', [])
        if business_logs:
            for i, log in enumerate(business_logs):
                status = log.get('BusinessStatus', 'Unknown')
                issues = log.get('Issues', 'No issues reported')
                icon = "🟢" if status == "Read" else "🔴" if status == "Unread" else "🟡"
                
                with st.expander(f"{icon} Log {i+1} - Status: {status}"):
                    st.write(f"**Status:** {status}")
                    st.write(f"**Issues:** {issues}")
        else:
            st.info("No business logs available")
    
    with col2:
        st.write("**👨‍💻 Tech Team Logs**")
        tech_logs = logs_data.get('tech_logs', [])
        if tech_logs:
            for i, log in enumerate(tech_logs):
                name = log.get('Name', 'Unknown')
                with st.expander(f"🔧 {name}"):
                    st.write(f"**System ID:** {log.get('SystemID', 'N/A')}")
                    st.write(f"**Username:** {log.get('UserName', 'N/A')}")
                    st.write(f"**Issues:** {log.get('IssueLogs', 'None')}")
        else:
            st.info("No tech logs available")
else:
    st.warning(f"⚠️ Could not load logs: {logs_data}")

st.divider()


st.subheader('📈 Aesthetic Trends')

if success_trends and trends_data:
    df_trends = pd.DataFrame(trends_data)
    
    if not df_trends.empty and 'Name' in df_trends.columns:
        chart = alt.Chart(df_trends).mark_bar(color="#A78BFA").encode(
            x=alt.X('PopularityPercent:Q', title='Popularity %'),
            y=alt.Y('Name:N', sort='-x', title='Aesthetic'),
            tooltip=['Name', 'PopularityPercent', 'Description']
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
else:
    st.info("No trend data available")

st.divider()


st.subheader('🔗 Quick Navigation')

col1, col2 = st.columns(2)

with col1:
    if st.button("🏢 Business Client Management →", use_container_width=True):
        st.switch_page('pages/23_Business_Client_Mgmt.py')

with col2:
    if st.button("📢 Notifications & Alerts →", use_container_width=True):
        st.switch_page('pages/25_Notif_Alert.py')


st.divider()
st.caption("💡 Data is loaded from the Flask API on page load. Refresh the page to update.")