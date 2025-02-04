import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

# Dependency to get DB session
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
