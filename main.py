import streamlit as st
import streamlit_authenticator as stauth
import os
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
            "password": user.password_hash
        } for user in users
    }
}

# Save credentials to a YAML file (streamlit_authenticator requires a file)
with open("credentials.yaml", "w") as file:
    yaml.dump({"credentials": credentials}, file)

# Read YAML for authenticator
with open("credentials.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)


# Extract user details from YAML structure
usernames = list(config["credentials"]["usernames"].keys())
names = [config["credentials"]["usernames"][user]["name"] for user in usernames]
passwords = [config["credentials"]["usernames"][user]["password"] for user in usernames]

# Create authenticator instance (cookie duration set for session persistence)
authenticator = stauth.Authenticate(
    names,
    usernames, 
    passwords,
    cookie_name="auth_cookie",
    key=COOKIE_PASS,  # Must match COOKIE_SECRET in .env
    cookie_expiry_days=10
)

# Toggle between Login and Register
#choice = st.radio("Select an option:", ["Login", "Register"])
show_login = True

# Toggle between Login and Register
if st.toggle("Login/Register", show_login):
    show_login = True
else:
    show_login = False
    

if show_login:
    name, authentication_status, username = authenticator.login("Login", location="main")
    print(f'Welcome {username}')

    # Handle login cases
    if authentication_status:
        st.write(f'{username} password: {config["credentials"]["usernames"][username]["password"]}')
        print(f'{username} password: {config["credentials"]["usernames"][username]["password"]}')
        login_response = us.login_user(username, config["credentials"]["usernames"][username]["password"])
        # Logout button
        
        authenticator.logout("Logout", "main")
        st.sidebar.write(f"Welcome, {username}!")
    elif authentication_status is False:
        st.error("Invalid username or password")

    elif authentication_status is None:
        st.warning("Please enter your username and password")

else:
    st.subheader("Register a new account")

    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Password", type="password", key="confirm_register_password")

    if st.button("Register"):
        if new_username in usernames:
            st.error("Username already exists. Choose another one.")
        elif new_password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Generate JWT token as password placeholder
            hashed_password = stauth.Hasher([new_password]).generate()[0]

            us.register_user(new_username, new_email, hashed_password)

            st.success("Registration successful! You can now log in.")




#st.sidebar.title("Navigation")
# st.sidebar.page_link("pages/1_Main_Dashboard.py", label="Main Dashboard")
# st.sidebar.page_link("pages/2_Income_Entry.py", label="Income")
# st.sidebar.page_link("pages/3_Users.py", label="Manage Users")



st.title("Finance Tracker Dashboard")

st.write("Money Management Made Easy")


# if __name__ == "__main__":
#     main()
