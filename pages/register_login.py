import streamlit as st
from services.user_service import register_user, login_user
from sqlalchemy.orm import Session


# Display content based on the selected page
def show_register_form(session: Session):
    st.header("Register")
    
    # Input Fields
    username = st.text_input("Username", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")

    if st.button("Submit",key="register_submit"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        
        response = register_user(username, email, password, session)
        if response["status"] == "error":
            st.error(response["message"])
        else:
            st.success(response["message"])
            st.session_state.page = "login"
            st.rerun()


def show_login_form(session: Session):
    st.header("Login")
    
    # Input Fields
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_submit"):
        response = login_user(username, password, session)
        if response["status"] == "error":
            st.error(response["message"])
        else:
            st.success(response["message"])

            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
       