import streamlit as st
import streamlit_authenticator as stauth
import os
#from streamlit_navigation_bar import st_navbar
#import pages as pg
#from services.authentication_service import login_user_form, register_user_form
from services.token_service import create_jwt, decode_jwt
from services import user_service as us
import yaml
from yaml.loader import SafeLoader


COOKIE_PASS = os.getenv("COOKIE_SECRET")
# Prompt Login Form on app start
users = us.view_users()


# Convert user data to match expected format for streamlit_authenticator
credentials = {
    "usernames": {
        user.username: {
            "email": user.email,
            "name": user.username,
            "password": create_jwt(user.user_id)  # Store JWT as "password"
        } for user in users
    }
}

# Save credentials to a YAML file (streamlit_authenticator requires a file)
with open("credentials.yaml", "w") as file:
    yaml.dump({"credentials": credentials}, file)

# Read YAML for authenticator
with open("credentials.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create authenticator instance (cookie duration set for session persistence)
authenticator = stauth.Authenticate(
    config["credentials"], 
    cookie_name="auth_cookie",
    key=COOKIE_PASS,  # Must match COOKIE_SECRET in .env
    cookie_expiry_days=10
)

name, authentication_status, username = authenticator.login("Login", location="main")

# Handle login cases
if authentication_status:
    # Logout button
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Logged in as {username}")

elif authentication_status is False:
    st.error("Invalid username or password")

elif authentication_status is None:
    st.warning("Please enter your username and password")




#st.sidebar.title("Navigation")
# st.sidebar.page_link("pages/1_Main_Dashboard.py", label="Main Dashboard")
# st.sidebar.page_link("pages/2_Income_Entry.py", label="Income")
# st.sidebar.page_link("pages/3_Users.py", label="Manage Users")





st.title("Finance Tracker Dashboard")

st.write("Money Management Made Easy")


# if __name__ == "__main__":
#     main()
