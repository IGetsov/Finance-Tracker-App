import os
from dotenv import load_dotenv
from persistence.connectors import get_session
from persistence.db_models import Role, User
from passlib.context import CryptContext
from typing import Dict
from persistence.mail_client import send_email


# Password Hashing setup
load_dotenv()

hash_scheme = os.getenv("HASH_SCHEME", "bcrypt")  # Default to bcrypt if not set
hash_deprecated = os.getenv("HASH_DEPRECATED", "auto")
hash_rounds = int(os.getenv("HASH_ROUNDS", 12))  # Work factor for bcrypt
COOKIE_PASS = os.getenv("COOKIE_SECRET")



# Set up password hashing context
pwd_context = CryptContext(
    schemes=[hash_scheme], 
    deprecated=hash_deprecated, 
    bcrypt__rounds=hash_rounds  # Adjust bcrypt work factor
)


def hash_password(password: str) -> str:
    """Hashes a password securely."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def view_roles():
    session = next(get_session())
    try:
        result = session.query(Role).all()
        return result
    finally:
        session.close()


def view_users():
    session = next(get_session())
    try:
        result = session.query(User).all()
        return result
    finally:
        session.close()

# Register function
def register_user(user_name: str, new_email: str, password: str) -> Dict[str, str]:
    session = next(get_session())
    try:
    # Check if user already exists and return warning message in the app
        is_user = session.query(User).filter(User.username == user_name).first()
        if is_user:
            return {
                "status": "error",
                "message": f'The username {user_name} is already registered! Please try different username.'
                }
        # If username does not exist - continue with creating the user
        hashed_password = hash_password(password)

        new_user = User(username=user_name, email=new_email, password_hash=hashed_password, role_id=100)
        session.add(new_user)
        session.commit()

        # Send confirmation email
        subject = "Welcome to Finance Tracker!"
        body = f"Hello {user_name},\n\nThank you for registering at Finance Tracker! You can now log in using the app.\n\nBest regards,\nFinance Tracker Team"
        
        email_sent = send_email(recepient_email=new_email, subject=subject, body=body)
        if email_sent:
            return {"status": "success", "message": f"You have registered successfully!\nA confirmation email will be sent shortly."}
        else:
            return {"status": "warning", "message": "User registered, but email sending failed."}
    finally:
        session.close()


# Login function
def login_user(user_name: str, password: str) -> Dict[str, str]:
    session = next(get_session())
    try:
        # Check if user name does not exist and raise an error
        is_user = session.query(User).filter(User.username == user_name).first()
        
        if not is_user or not verify_password(password, is_user.password_hash):
            return {
                "status": "error",
                "message": "Invalid username or password! Please try again."
            }
        return {
            "status": "success",
            "message": f"Welcome {user_name}!"
        }
    finally:
        session.close()

  
