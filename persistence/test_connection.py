from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from services import user_service as us



load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def test_connection():
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        # Test a simple query
        result = us.view_roles(session)
        [print(f'{r.role_id} {r.description}') for r in result]
        print("Connection test successful:", result)
    except Exception as e:
        print("Connection test failed:", e)
    finally:
        session.close()


if __name__ == "__main__":
    test_connection()
