import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('System Admin Home Page')

if st.button('Dashboard & Overview',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Dashboard_Overview.py')

if st.button('Business Client Management',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Business_Client_Mgmt.py')

if st.button('Wishlist Matching',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/24_Wishlist_Match.py')

if st.button('Notifications & Alerts',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/25_Notif_Alert.py')

if st.button('Settings & Permissions',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/26_Setting_Permission.py')