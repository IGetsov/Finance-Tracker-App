import os
import streamlit as st
from dotenv import load_dotenv
import streamlit_authenticator as asuth
from services.user_service import login_user, register_user



load_dotenv()

COOKIE_PASS = os.getenv("COOKIE_SECRET")


# Initialize cookie manager

def authenticate(username, password):
    """Check if username and password are correct."""
    response = login_user(username, password)
    if response["status"] == "error":
        return st.error(response["message"])
    else:
        return response


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



def load_session():
    """Retrieve login state from cookies on app startup."""
    if "authenticated" in cookies and cookies["authenticated"] == "true":
        st.session_state.authenticated = True
        st.session_state.username = cookies.get("username")
    else:
        st.session_state.authenticated = False
        st.session_state.username = None