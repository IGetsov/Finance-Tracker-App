from datetime import date
from models.income_models import IncomeCreate
from persistence.connectors import get_session
from persistence.db_models import Frequency, Income, IncomeCategory


def get_income_categories():
    """Display all Income categories"""
    session = next(get_session())
    try:
        categories = session.query(IncomeCategory).all()
        result = {category.id: category.income_description for category in categories}
        print(f"THIS IS THE OUTPUT: {result}")
        return result
    finally:
        session.close()


def get_frequencies():
    """Display all frequencies"""
    session = next(get_session())
    try:
        frequencies = session.query(Frequency).all()
        return {frequency.id: frequency.frequency_description for frequency in frequencies}
    finally:
        session.close()


def add_income(user_id: int, amount: float, income_type: int, frequency: int):
    """Create new Income record for relevant user ID"""
    session = next(get_session())
    
    try:
        # Validate data types
        new_income = IncomeCreate(
            user_id=user_id,
            amount=amount,
            month=date.today(),
            income_type=int(income_type),
            income_frequency=int(frequency)
        )

        # Get Income Type and Frequency as objects
        income_type_obj = session.query(IncomeCategory).filter_by(id=new_income.income_type).first()
        income_frequency_obj = session.query(Frequency).filter_by(id=new_income.income_frequency).first()

        if not income_type_obj or not income_frequency_obj:
            raise ValueError("Invalid income type or frequency selection.")
        
        income_to_add = Income(
            user_id=user_id,
            amount_encrypted=str(new_income.amount),  # Convert to bytes
            income_type=income_type_obj,
            income_frequency=income_frequency_obj,
            month=new_income.month
        )
        session.add(income_to_add)
        session.commit()
        print(income_to_add)
        return income_to_add
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    
def edit_income(income_id: int, user_id: int, amount: float, income_type: int, frequency: int, month: date):
    """Edit Income record by income ID and user ID"""
    session = next(get_session())

    try:
        income_record = session.query(Income).filter_by(id=income_id, user_id=user_id).first()
        if not income_record:
            raise ValueError("Income record not found!")

        # Get Income Type and Frequency as objects
        income_type_obj = session.query(IncomeCategory).filter_by(id=income_type).first()
        income_frequency_obj = session.query(Frequency).filter_by(id=frequency).first()

        if not income_type_obj or not income_frequency_obj:
            raise ValueError("Invalid income type or frequency selection.")

        # Values for update
        income_record.amount_encrypted = str(amount)
        income_record.income_type = income_type_obj
        income_record.income_frequency = income_frequency_obj
        income_record.month = month

        session.commit()
        return income_record
    
    except Exception as e:
        session.rollback()
        raise e
    
    finally:
        session.close()


def delete_income(income_id: int, user_id: int):
    """Delete Income record by income ID and user ID"""
    session = next(get_session())
    try:
        # Find the income record
        income_record = session.query(Income).filter_by(id=income_id, user_id=user_id).first()

        if not income_record:
            raise ValueError("Income record not found or does not belong to the user.")

        # Delete income record
        session.delete(income_record)
        session.commit()

        return {"message": "Income deleted successfully!"}

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def get_user_incomes(user_id: int):
    """Get all income records by user ID"""
    session = next(get_session())
    try:
        return session.query(Income).filter_by(user_id=user_id).all()
    except Exception as e:
        raise e
    finally:
        session.close()