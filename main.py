import streamlit as st
from pages.register_login import show_register_form, show_login_form
from persistence.connectors import get_db

# Initialize session state Default to home screen
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation helper
def navigate_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()


st.sidebar.title("Navigation")
st.sidebar.page_link("pages/1_Main_Dashboard.py", label="Main Dashboard")
#st.sidebar.page_link("pages/3_Users.py", label="Manage Users")

st.title("Finance Tracker Dashboard")

st.write("Money Management Made Easy")


col1, col2 = st.columns(2)
with col1:
    if st.button('Register'):
        navigate_to_page('register')
with col2:
    if st.button('Login'):
        navigate_to_page('login')


# Get a database session
db = next(get_db())

# Render the selected page
if st.session_state.page == "register":
    show_register_form(db)
elif st.session_state.page == "login":
    show_login_form(db)
