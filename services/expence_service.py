from models.expense_models import ExpenseCreate
from persistence.connectors import get_session
from persistence.db_models import Expense, ExpenseCategory, ExpenseSubCategory


def get_expence_categories():
    """Display all Expence categories"""
    session = next(get_session())
    try:
        categories = session.query(ExpenseCategory).all()
        result = {category.category_id: category.category_name for category in categories}
        return result
    finally:
        session.close()


def get_expense_sub_categories(category_id: int):
    """Get relevant sub categories by category_id"""
    session = next(get_session())
    try:
        sub_categories = session.query(ExpenseSubCategory).filter(ExpenseSubCategory.category_id == category_id)
        result = {sub_category.sub_category_id: sub_category.sub_category_name for sub_category in sub_categories}
        print(f"RETURN FROM SUB CATEGORIES: {result}")
        return result
    finally:
        session.close()


def add_expense(user_id: int, month, amount: float, category_id: int, sub_category_id: int, description: str):
    """Create new Expense record for relevant user ID"""
    try:
        session = next(get_session())
        # Validate data types
        new_expense = ExpenseCreate(
            user_id=user_id, 
            month=month,
            amount=amount,
            category_id=category_id,
            description=description
        )
      
 
        expense_to_add = Expense(
            user_id=user_id,
            month=month,
            amount=amount,
            category_id=category_id,
            sub_category_id=sub_category_id,
            description=description
        )
        
        session.add(expense_to_add)
        session.commit()
        return True
    
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    
    finally:
        session.close()