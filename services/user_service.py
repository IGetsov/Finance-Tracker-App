import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from persistence.db_models import Role, User
from passlib.context import CryptContext

# Password Hashing setup
load_dotenv()

hash_scheme = os.getenv("HASH_SCHEME", "bcrypt")  # Default to bcrypt if not set
hash_deprecated = os.getenv("HASH_DEPRECATED", "auto")
hash_rounds = int(os.getenv("HASH_ROUNDS", 12))  # Work factor for bcrypt

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


def view_roles(session: Session):
    result = session.query(Role).all()
    return result


def view_users(session: Session):
    result = session.query(User).all()
    return result


def register_user(user_name: str, new_email: str, password: str, session: Session):
    # Check if user already exists and return warning message in the app
    is_user = session.query(User).filter(User.username == user_name).first()
    if is_user:
        return {
            "status": "error",
            "message": f'The username {user_name} is already registered! Please try different username.'
            }
    # If username does not exist - continue with creating the user
    hashed_password = hash_password(password)

    new_user = User(username=user_name, email=new_email, password_hash=hashed_password, role_id=1)
    session.add(new_user)
    session.commit()
    return {
        "status": "success",
        "message": "You have registered successfuly! Enjoy the app."
    }


def login_user(user_name: str, password: str, session: Session):
    # Check if user name does not exist and raise an error
    is_user = session.query(User).filter(User.username == user_name).first()
    
    if not is_user or not pwd_context.verify_password(password, is_user.password_hash):
        return {
            "status": "error",
            "message": "Invalid username or password! Please try again."
        }
    return {
        "status": "success",
        "message": f"Welcome {user_name}!"
    }
    
