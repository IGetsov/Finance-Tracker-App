from models.income_models import IncomeCreate
from persistence.connectors import get_session
from persistence.db_models import Frequency, Income, IncomeCategory


def get_income_categories():
    session = next(get_session())
    try:
        categories = session.query(IncomeCategory).all()
        result = {category.id: category.income_description for category in categories}
        print(f"THIS IS THE OUTPUT: {result}")
        return result
    finally:
        session.close()


def get_frequencies():
    session = next(get_session())
    try:
        frequencies = session.query(Frequency).all()
        return {frequency.id: frequency.frequency_description for frequency in frequencies}
    finally:
        session.close()


def add_income(user_id: int, amount: float, income_type: int, frequency: int):
    session = next(get_session())
    try:
        new_income = IncomeCreate()
        return new_income
    finally:
        session.close()