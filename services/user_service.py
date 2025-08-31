from datetime import timedelta
from fastapi import HTTPException
from persistence.connectors import get_session
from persistence.db_models import Role, User
from typing import Dict
from persistence.mail_client import send_email
from services.authentication_service import create_access_token, hash_password, verify_password


def register_user(username: str, email: str, password: str):
    session = next(get_session())
    try:
        if session.query(User).filter(User.username == username).first():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        hashed_pw = hash_password(password)
        new_user = User(username, email, password_hash=hashed_pw)
        session.add(new_user)
        session.commit()
        return new_user
    finally:
        session.close()


def login_user(username: str, password: str):
    session = next(get_session())
    try:
        user = session.query(User).filter(User.username == username).first()
        if not user or not verify_password(password=password, hashed_password=user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=60))
        return {"access_token": token, "token_type": "bearer"}
    finally:
        session.close()
 

def view_roles():
    """Return recordset for all user roles"""
    session = next(get_session())
    try:
        result = session.query(Role).all()
        return result
    finally:
        session.close()


def view_users():
    """Return recordset for all users"""
    session = next(get_session())
    try:
        result = session.query(User).all()
        return result
    finally:
        session.close()

def view_user_by_name(username: str):
    """Return user record if username matched"""
    sesssion = next(get_session())
    try:
        result = sesssion.query(User).filter(User.username == username).first()
        return result
    finally:
        sesssion.close()


# Register function
def register_user(user_name: str, new_email: str, hashed_password: str) -> Dict[str, str]:
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
        is_user = view_user_by_name(user_name)
        
        if not is_user or not verify_password(password, is_user.password_hash):
            return {
                "status": "error",
                "message": "Invalid username or password! Please try again."
            }
        return is_user
    finally:
        session.close()

  
