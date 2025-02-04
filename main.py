import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager
from streamlit_navigation_bar import st_navbar
import pages as pg
from services.token_service import create_jwt
from services.user_service import login_user, register_user
from styles.navbar_styles import styles, options


load_dotenv()

# Initialize Cookie Manager in the UI layer
COOKIE_PASS = os.getenv("COOKIE_SECRET")
cookies = EncryptedCookieManager(prefix="auth_", password=COOKIE_PASS)

# Ensure cookies are ready
if not cookies.ready():
    st.stop()


# Initialize session state Default to home screen
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation helper
def navigate_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()


# /// Adding Login And Register functions in order to keep cookies session
# Display content based on the selected page
def register_user_form():
    st.header("Register")
    
    # Input Fields
    username = st.text_input("Username", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")

    if st.button("Submit",key="register_submit"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        
        response = register_user(username, email, password)
        if response["status"] == "error":
            st.error(response["message"])
        else:
            st.success(response["message"])
            st.session_state.page = "login"
            st.rerun()


def login_user_form():
    st.header("Login")
    
    # Input Fields
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_submit"):
        response = login_user(username, password)
        if response["status"] == "error":
            st.error(response["message"])
        else:
            st.success(response["message"])
            # Generate JWT
            token = create_jwt(user_id=response["user_id"])
            cookies["jwt_token"] = token
            cookies.save()

            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
       

def logout():
    st.header("Logout")
    cookies["jwt_token"] = ""
    cookies.save()
    st.success("Logged out successfully! Refreshing...")
    st.rerun()


col1, col2, col3, col4 = st.columns(4)
with col3:
    if st.button('Register'):
        register_user_form()
with col4:
    if st.button("Login"):
        login_user_form()

st.sidebar.title("Navigation")
st.sidebar.page_link("pages/1_Main_Dashboard.py", label="Main Dashboard")
st.sidebar.page_link("pages/2_Income_Entry.py", label="Income")
# st.sidebar.page_link("pages/3_Users.py", label="Manage Users")

st.title("Finance Tracker Dashboard")

st.write("Money Management Made Easy")



