from datetime import date
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
    print(f"Income type {int(income_type)}\nFrequency {int(frequency)}")
    try:
        # Validate data types
        new_income = IncomeCreate(
            user_id=user_id,
            amount=amount,
            month=date.today(),
            income_type=int(income_type),
            income_frequency=int(frequency)
        )
        
        income_to_add = Income(
            user_id=user_id,
            amount_encrypted=str(new_income.amount),  # Convert to bytes
            income_type=new_income.income_type,
            income_frequency=new_income.income_frequency,
            month=new_income.month
        )
        session.add(income_to_add)
        session.commit()
        print(income_to_add)
        return income_to_add
    finally:
        session.close()