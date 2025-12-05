import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import altair as alt

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Dashboard and Overview Page')

st.write('\n\n')
st.write('## Top KPI')
col1, col2, col3 = st.columns(3) 
with col1:
    st.metric(label="Total Users", value="46,500")  
with col2:
    st.metric(label="Total Business Clients", value="96")   
with col3:
    st.metric(label="Pending Approvals", value="2", help="Users / Retailers") 
st.divider()

st.write('\n\n')
st.write('## Weekly New Signups')
st.subheader("Weekly New Signups")
st.write("Users / Businesses / Daily Outfits Uploads / Wishlist Conversions")

df = pd.DataFrame({
    "Date": ["Su", "M", "T", "W", "Th", "F", "S"],
    "Users": [550, 625, 475, 600, 350, 750, 675]
})
chart = (
    alt.Chart(df)
    .mark_bar(color="#A78BFA")
    .encode(
        x=alt.X("Date", sort=["Su", "M", "T", "W", "Th", "F", "S"]),
        y="Users"
    )
)
st.altair_chart(chart, use_container_width=True)

df = pd.DataFrame({
    "Date": ["Su", "M", "T", "W", "Th", "F", "S"],
    "Businesses": [300, 450, 400, 500, 250, 600, 550]
})
chart = (
    alt.Chart(df)
    .mark_bar(color="#A78BFA")
    .encode(
        x=alt.X("Date", sort=["Su", "M", "T", "W", "Th", "F", "S"]),
        y="Businesses"
    )
)
st.altair_chart(chart, use_container_width=True)

df = pd.DataFrame({
    "Date": ["Su", "M", "T", "W", "Th", "F", "S"],
    "Daily Outfit Uploads": [220, 150, 190, 160, 80, 200, 325]
})
chart = (
    alt.Chart(df)
    .mark_bar(color="#A78BFA")
    .encode(
        x=alt.X("Date", sort=["Su", "M", "T", "W", "Th", "F", "S"]),
        y="Daily Outfit Uploads"
    )
)
st.altair_chart(chart, use_container_width=True)

df = pd.DataFrame({
    "Date": ["Su", "M", "T", "W", "Th", "F", "S"],
    "Wishlist Conversions": [400, 250, 335, 420, 550, 600, 750]
})
chart = (
    alt.Chart(df)
    .mark_bar(color="#A78BFA")
    .encode(
        x=alt.X("Date", sort=["Su", "M", "T", "W", "Th", "F", "S"]),
        y="Wishlist Conversions"
    )
)
st.altair_chart(chart, use_container_width=True)