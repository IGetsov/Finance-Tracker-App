import streamlit as st
import pages

st.sidebar.title("Navigation")
st.sidebar.page_link("pages/1_Main_Dashboard.py", label="Main Dashboard")
#st.sidebar.page_link("pages/3_Users.py", label="Manage Users")

st.title("Finance Tracker Dashboard")
