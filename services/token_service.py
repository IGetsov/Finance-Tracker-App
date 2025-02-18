from datetime import datetime, timedelta
import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
COOKIE_PASS = os.getenv("COOKIE_SECRET")


# Function to create JWT token



# Function to decode JWT token
