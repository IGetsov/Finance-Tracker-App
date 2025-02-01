from sqlalchemy.orm import Session
from persistence.db_models import Role, User


def view_roles(session: Session):
    result = session.query(Role).all()
    return result


def view_users(session: Session):
    result = session.query(User).all()
    return result