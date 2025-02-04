from models.income_models import IncomeCreate
from persistence.connectors import get_session
from persistence.db_models import Frequency, Income, IncomeCategory

def get_income_categories():
    with get_session() as session:
        categories = session.query(IncomeCategory).all()
        result = {category.id: category.description for category in categories}
        print(result)
        return result


def get_frequencies():
    with get_session() as session:
        frequencies = session.query(Frequency).all()
        return {frequency.id: frequency.description for frequency in frequencies}


def add_income(user_id: int, amount: float, income_type: int, frequency: int):
    with get_session() as session:
        new_income = IncomeCreate()