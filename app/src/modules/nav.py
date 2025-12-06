# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Pages for Role of Consumer ------------------------
def ConsumerHomeNav():
    st.sidebar.page_link(
        "pages/00_Consumer_Home.py", label="Consumer Home", icon="🏠"
    )

def ConsumerWishlistNav():
    st.sidebar.page_link(
        "pages/00_Consumer_Wishlist.py", label="My Wishlist", icon="💜"
    )

def ConsumerClosetNav():
    st.sidebar.page_link("pages/00_Consumer_Closet.py", label="My Closet", icon="👔")

def ConsumerProfileNav():
    st.sidebar.page_link("pages/00_Consumer_Profile.py", label="Profile", icon="👤")

## ------------------------ Examples for Role of usaid_worker ------------------------

def usaidWorkerHomeNav():
    st.sidebar.page_link(
      "pages/10_USAID_Worker_Home.py", label="USAID Worker Home", icon="🏠"
    )

def NgoDirectoryNav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")

def AddNgoNav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")

def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")

def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )

def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


#### ------------------------ Pages for Role of Business Ownwer ------------------------
def BusinessInventoryNav():
    st.sidebar.page_link("pages/38_Business_Inventory.py", label="Inventory", icon="📦")
def BusinessHomeNav():
    st.sidebar.page_link("pages/_36_Business_Home.py", label="Home", icon="🖥️")
def BusinessWishlistNav():
    st.sidebar.page_link("pages/39_Business_Wishlist.py", label="Wishlist", icon="💜")


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
def Dashboard():
    st.sidebar.page_link("pages/22_Dashboard_Overview.py", label="Dashboard & Overview", icon="📑")
def BCMgmt():
    st.sidebar.page_link("pages/23_Business_Client_Mgmt.py", label="BC Management", icon="🧑‍💼")
def WishMatch():
    st.sidebar.page_link("pages/24_Wishlist_Match.py", label="Wishlist Matching", icon="👚")
def NotifAlert():
    st.sidebar.page_link("pages/25_Notif_Alert.py", label="Notifications & Alerts", icon="🚨")
def SettingPerm():
    st.sidebar.page_link("pages/26_Setting_Permission.py", label="Settings & Permissions", icon="⚙️")

### ------------------------ Data Analyst Role -------------------------------
def DataAnalystHomeNav():
    st.sidebar.page_link("pages/31_Data_Analyst_Home.py", label="Data Analyst Home", icon="🏠")
def DataAnalystBrandsNav():
    st.sidebar.page_link("pages/32_Data_Analyst_Brands.py", label="Brands to Watch", icon="🏷️")
def DataAnalystTrendingNav():
    st.sidebar.page_link("pages/33_Data_Analyst_Trending.py", label="Current Trends", icon="📈")
def DataAnalystWishListsNav():
    st.sidebar.page_link("pages/34_Data_Analyst_Wish_List.py", label="Wish Lists", icon="❤️")
def DataAnalystClosetStaplesNav():
    st.sidebar.page_link("pages/35_Data_Analyst_Closet_Staples.py", label="Closet Staples", icon="🗄️")

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/cluelessLogo.png", width=130)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show wishlist, closet, and profile links if the user is a consumer role.
        if st.session_state["role"] == "consumer":
            ConsumerHomeNav()
            ConsumerProfileNav()
            ConsumerClosetNav()
            ConsumerWishlistNav()
            

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "usaid_worker":
            usaidWorkerHomeNav()
            NgoDirectoryNav()
            AddNgoNav()
            PredictionNav()
            ApiTestNav()
            ClassificationNav()
            

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()
            Dashboard()
            BCMgmt()
            WishMatch()
            NotifAlert()
            SettingPerm()

        # If the user is an business owner, give them access to the business pages
        if st.session_state["role"] == "business_owner":
            BusinessInventoryNav()
            BusinessHomeNav()
            BusinessWishlistNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
