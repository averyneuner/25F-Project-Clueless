import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Business Notifications",
    page_icon="🔔",
    layout="wide",
)

SideBarLinks()

API_BASE = "http://web-api:4000"

if "first_name" not in st.session_state:
    st.session_state["first_name"] = "Guest"

if "role" not in st.session_state:
    st.session_state["role"] = "business_owner"

if "business_id" not in st.session_state:
    st.session_state["business_id"] = 40 


def get_business_id() -> int:
    return st.session_state.get("business_id", 40)

def fetch_notifications(business_id: int):
    """
    GET /business/<business_id>/notifications
    """
    url = f"{API_BASE}/business/{business_id}/notifications"
    try:
        resp = requests.get(url, timeout=5)

        if resp.status_code == 404:
            try:
                data = resp.json()
                return [], data.get("error", "Business not found (404)")
            except Exception:
                return [], "Business not found (404)"

        resp.raise_for_status()
        return resp.json(), None
    except requests.RequestException as e:
        return [], f"Request error: {e}"
    except ValueError:
        return [], "API did not return valid JSON for notifications"


def send_notification(business_id: int, message: str, status: str = "Sent"):
    """
    POST /business/<business_id>/notifications
    body: { "message": str, "status": str }
    """
    url = f"{API_BASE}/business/{business_id}/notifications"
    payload = {"message": message, "status": status}
    try:
        resp = requests.post(url, json=payload, timeout=5)
        if resp.status_code >= 400:
            try:
                data = resp.json()
                return False, data.get("error", f"HTTP {resp.status_code}")
            except Exception:
                return False, f"HTTP {resp.status_code}"
        return True, None
    except requests.RequestException as e:
        return False, f"Request error: {e}"


def delete_notification(business_id: int, notification_id: int):
    """
    DELETE /business/<business_id>/notifications/<notification_id>
    """
    url = f"{API_BASE}/business/{business_id}/notifications/{notification_id}"
    try:
        resp = requests.delete(url, timeout=5)
        if resp.status_code >= 400:
            try:
                data = resp.json()
                return False, data.get("error", f"HTTP {resp.status_code}")
            except Exception:
                return False, f"HTTP {resp.status_code}"
        return True, None
    except requests.RequestException as e:
        return False, f"Request error: {e}"


#actual page code
business_id = get_business_id()

st.title("Business Notifications 🔔")
st.caption(f"Business ID: `{business_id}`")

left, right = st.columns([1, 2])

#sending notifs 
with left:
    st.subheader("Create a notification")

    with st.form("send_notification_form", clear_on_submit=True):
        message = st.text_area(
            "Message",
            placeholder="Write the notification message you want to send...",
            height=120,
        )
        status = st.selectbox(
            "Status",
            options=["Sent", "Pending", "Resolved"],
            index=0,
            help="How you want this notification to be marked in the system.",
        )

        submitted = st.form_submit_button("Send notification")

        if submitted:
            if not message.strip():
                st.error("Message cannot be empty.")
            else:
                ok, err = send_notification(business_id, message.strip(), status)
                if ok:
                    st.success("Notification sent successfully.")
                    st.rerun()
                else:
                    st.error(f"Could not send notification: {err}")

# manage notifs 
with right:
    st.subheader("Existing notifications")

    notifications, notif_err = fetch_notifications(business_id)

    if notif_err:
        st.error(f"Could not load notifications: {notif_err}")
    elif not notifications:
        st.info("No notifications found for this business.")
    else:
        df = pd.DataFrame(notifications)
        preferred_cols = [
            "NotificationID",
            "Message",
            "Status",
            "CompanyName",
            "ContactEmail",
        ]
        cols = [c for c in preferred_cols if c in df.columns] + [
            c for c in df.columns if c not in preferred_cols
        ]
        df = df[cols]

        with st.expander("View notifications as table", expanded=False):
            st.dataframe(df, use_container_width=True)

        st.markdown("### Manage notifications")

        for idx, notif in enumerate(notifications):
            notif_id = notif.get("NotificationID")
            msg = notif.get("Message", "")
            status = notif.get("Status", "")
            company = notif.get("CompanyName", "")
            email = notif.get("ContactEmail", "")

            with st.container(border=True):
                top_cols = st.columns([3, 1])
                with top_cols[0]:
                    st.markdown(f"**#{notif_id} – {msg[:80]}**")
                with top_cols[1]:
                    st.markdown(f"**Status:** {status}")

                st.caption(
                    f"Company: {company or 'N/A'}  •  Contact: {email or 'N/A'}"
                )

                if st.button(
                    "🗑 Delete notification",
                    key=f"delete_notif_{idx}_{notif_id}",
                    use_container_width=True,
                ):
                    ok, err = delete_notification(business_id, notif_id)
                    if ok:
                        st.success("Notification deleted.")
                        st.rerun()
                    else:
                        st.error(f"Could not delete notification: {err}")
