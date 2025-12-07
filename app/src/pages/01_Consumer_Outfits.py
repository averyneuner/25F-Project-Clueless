import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import time
from modules.nav import SideBarLinks

st.set_page_config(layout= 'wide')

API_BASE_URL = "http://web-api:4000"

# API retrival functions: 

# 1) get the customer's closet
def get_customer_closet(customer_id):
    try: 
        response = requests.get(f"{API_BASE_URL}/customer/{customer_id}/closets", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend at {API_BASE_URL}. Is your Flask server running?")
        return None
    except requests.exceptions.Timeout:
        st.error(f"❌ Request timed out. Backend may be slow or not responding.")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            st.error(f"❌ Customer ID {customer_id} not found in database.")
        else:
            st.error(f"❌ HTTP Error: {e.response.status_code} - {e.response.json().get('error', 'Unknown error')}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error")
        return None
    

# 2) add an outfit to the closet
def add_closet_outfit(customer_id, closet_id, outfit_id):
    try:
        response = requests.post(
            f"{API_BASE_URL}/customer/{customer_id}/closets/{closet_id}/outfit/{outfit_id}"
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Error adding item: {e.response.json().get('error', 'Unknown error')}")
        try:
            error_data = e.response.json()
            error_msg = error_data.get('error', error_msg)
        except:
            try:
                if e.response.text:
                    error_msg = e.response.text[:100]
            except:
                pass
        st.error(f"❌ Error adding Outfit.")
        return None
    except Exception as e:
        st.error(f"❌ Error")
        return None

# 3) adds a clothing item to an outfit.
def create_outfit(outfit_data):
    try:
        response = requests.post(
            f"{API_BASE_URL}/outfits",
            json=outfit_data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Error creating outfit")
        return None
    except Exception as e:
        st.error(f"❌ Error")
        return None

# 4) delete an outfit
def delete_outfit(outfit_id):
    try:
        response = requests.delete(
            f"{API_BASE_URL}/outfits/{outfit_id}",
            timeout=5
        )
        response.raise_for_status()
        try:
            return response.json()
        except:
            return {"message": "Success"}
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend")
        return None
    except requests.exceptions.Timeout:
        st.error(f"❌ Request timed out")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Error deleting outfit")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected Error")
        return None



# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

if 'customer_id' not in st.session_state:
    st.session_state['customer_id'] = 13
    st.session_state['closet_id'] = 115
    st.session_state['first_name'] = 'Rachel'
    st.session_state['last_name'] = 'Green'
    st.session_state['email'] = 'rachel.green@example.com'

# styling w CSS:
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #A78BFA;
        color: #1E293B;
        border-radius: 20px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
    }
    .stButton > button:hover {
        background-color: #9370DB;
        color: #E2E8F0;
    }
    .outfit-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #DDD6FE;
        margin-bottom: 15px;
        background-color: #F9FAFB;
    }
    .outfit-badge {
        display: inline-block;
        padding: 5px 10 px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        background-color: #DDD6FE;
        color: #5B21B6;
        margin-right: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title(f"👗 {st.session_state['first_name']}'s Outfits")
st.markdown("View and manage your outfits collections.")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Back to Closet", key="back_button"):
        st.switch_page("pages/00_Consumer_Closet.py")

st.divider()


# need to get the data:
closet_data = get_customer_closet(st.session_state['customer_id'])

if closet_data:
    outfits = closet_data.get('outfits', [])

    # case 1: when the closet is empty (no items yet)
    if not outfits:
        st.info("Your closet has no outfits yet. Add some outfits to get started!")

        with st.expander(" Add Your First Outfit", expanded= True):
            with st.form("add_first_outfit"):
                col1, col2 = st.columns(2)

                with col1:
                    nickname = st.text_input("Outfit Nickname*", placeholder="e.g., Favorite Summer Casual Fit")
                    description = st.text_area("Description*", placeholder="Describe this outfit...")

                with col2:
                    st.info("💡 After creating the outfit, you can add clothing items to it!")

                submit = st.form_submit_button("Create Outfit")
                if submit:
                    if not all ([nickname, description]):
                        st.error("Need all required data to be filled in.")
                    else:
                        outfit_data = {
                            "nickname": nickname,
                            "description": description
                        }

                        result = create_outfit(outfit_data)
                        if result: 
                            new_outfit_id = result.get('OutfitID')
                            st.success(f"✅ Outfit Created! (ID: {new_outfit_id})")
                            add_result = add_closet_outfit(
                                st.session_state['customer_id'],
                                st.session_state['closet_id'],
                                new_outfit_id
                            )
                            if add_result:
                                st.toast("🥳 Outfit added to your closet!")
                                st.rerun()
    
    # case 2: have outfits in your closet:
    else:
        st.subheader(f"👔 Total Outfits: {len(outfits)}")

        # group outfit info and outfits by OutfitID (each outfit w its corresponding items)
        outfit_dict = {}
        for outfit in outfits:
            outfit_id = outfit['OutfitID']
            if outfit_id not in outfit_dict:
                outfit_dict[outfit_id] = {
                    'name': outfit['OutfitName'],
                    'items': []
                }
            outfit_dict[outfit_id]['items'].append(outfit['ItemName'])

        st.divider()

        # display the outfits:
        if not outfit_dict:
            st.warning("No outfits to display.")
        else:
            st.markdown(f"**Showing {len(outfit_dict)} outfits**")
            cols = st.columns(2)

            for idx, (outfit_id, outfit_data) in enumerate(outfit_dict.items()):
                with cols[idx % 2]:
                    with st.container(border=True):
                        header_col1, header_col2 = st.columns([4, 1])
                        with header_col1:
                            st.markdown(f"### 👔 {outfit_data['name']}")
                            st.markdown(
                                f'<span class="outfit-badge"> Outfit ID: {outfit_id}</span>',
                                unsafe_allow_html=True
                            )

                            st.write("")
                            st.markdown("**Items in this outfit:**")

                            if outfit_data['items']:
                                for item in outfit_data['items']:
                                    st.markdown(f"- {item}")
                            else:
                                st.info("No items in this outfit yet!")

                            st.write("")
                            st.metric("Total Items", len(outfit_data['items']))
                        
                        with header_col2:
                            if st.button("🗑️ Delete", key=f"delete_{outfit_id}", help="Delete Outfit"):
                                if st.session_state.get(f'confirm_delete_{outfit_id}'):
                                    result = delete_outfit(outfit_id)
                                    if result:
                                        st.success("✅ Outfit deleted!")
                                        time.sleep(1.5)
                                        st.rerun()
                                else:
                                    st.session_state[f'confirm_delete_{outfit_id}'] = True
                                    st.rerun()

                        # Show confirmation warning if delete was clicked
                        if st.session_state.get(f'confirm_delete_{outfit_id}'):
                            st.warning("⚠️ Click delete again to confirm")
                            if st.button("Cancel", key=f"cancel_delete_{outfit_id}"):
                                st.session_state[f'confirm_delete_{outfit_id}'] = False
                                time.sleep(1.5)
                                st.rerun()


            st.divider()
            
            # add a new outfit section:
            with st.expander("➕ Add New Outfit"):
                tab1, = st.tabs(["Create New Outfit"])

                # create a new outfit
                with tab1:
                    with st.form("create_new_outfit"):
                        st.markdown("**Create a brand new outfit & add it to your closet**")

                        col1, col2 = st.columns(2)

                        with col1:
                            nickname = st.text_input("Outfit Nickname*", placeholder="e.g. Monday Gym Sesh")
                        
                        with col2:
                            description = st.text_area("Description*", placeholder="Describe this outfit...")

                        submit_new = st.form_submit_button("Create & Add to Closet")
                        if submit_new:
                            if not all([nickname, description]):
                                st.error("Need to fill in all required fields.")
                            else:
                                outfit_data = {
                                    "nickname": nickname, 
                                    "description": description
                                }

                                result = create_outfit(outfit_data)
                                if result:
                                    new_outfit_id = result.get('OutfitID')
                                    st.success(f"✅ Outfit Created! (ID: {new_outfit_id})")

                                    add_result = add_closet_outfit(
                                        st.session_state['customer_id'],
                                        st.session_state['closet_id'],
                                        new_outfit_id
                                    )

                                    if add_result:
                                        st.toast("✅ Outfit added to your closet!")
                                        st.rerun()
else:
    st.error("Unable to load closet data.")


# Some quick sidebar closet data stats:
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")

    if closet_data:
        outfits = closet_data.get('outfits', [])

        if outfits:
            unique_outfits = len(set([o['OutfitID'] for o in outfits]))
            total_items_in_outfits = len(outfits)

            st.metric("Total Outfits", unique_outfits)
            st.metric("Total Items in Outfits", total_items_in_outfits)

            outfit_counts = {}
            for outfit in outfits:
                outfit_id = outfit['OutfitID']
                outfit_name = outfit['OutfitName']
                if outfit_id not in outfit_counts:
                    outfit_counts[outfit_id] = {'name': outfit_name, 'count': 0}
                outfit_counts[outfit_id]['count'] += 1
            
            if outfit_counts:
                most_items_outfit = max(outfit_counts.items(), key=lambda x: x[1]['count'])
                st.markdown("**Largest Outfit**")
                st.text(f"{most_items_outfit[1]['name']}")
                st.text(f"({most_items_outfit[1]['count']} items)")

        else: 
            st.info("No outfits yet!")

    st.markdown("---")
    if st.button("🔄 Refresh Data"):
        st.rerun()
