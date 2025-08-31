from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from jose import JWSError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer



load_dotenv()

COOKIE_PASS = os.getenv("COOKIE_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_TOKEN_TIME = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Password util functions

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


# JWT functions

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expiration = datetime.timezone.utc() + (expires_delta or (timedelta(minutes=os.ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expiration})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWSError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# # Display content based on the selected page
# def register_user_form():
#     st.header("Register")
    
#     # Input Fields
#     username = st.text_input("Username", key="register_username")
#     email = st.text_input("Email", key="register_email")
#     password = st.text_input("Password", type="password", key="register_password")
#     confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")

#     if st.button("Submit",key="register_submit"):
#         if password != confirm_password:
#             st.error("Passwords do not match!")
        
#         response = register_user(username, email, password)
#         if response["status"] == "error":
#             st.error(response["message"])
#         else:
#             st.success(response["message"])
#             st.session_state.page = "login"
#             st.rerun()



