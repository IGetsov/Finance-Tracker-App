import os
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from services import user_service as us

# Load the secret key for cookie encryption
COOKIE_PASS = os.getenv("COOKIE_SECRET")


def get_authenticator():
    """Initialize and return Streamlit Authenticator."""
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

    # Create authenticator instance
    authenticator = stauth.Authenticate(
        names,
        usernames, 
        passwords,
        cookie_name="auth_cookie",
        key=COOKIE_PASS,  
        cookie_expiry_days=10
    )

    return authenticator, config
