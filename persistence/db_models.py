from sqlalchemy import TIMESTAMP, Column, Date, DateTime, Float, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import relationship
from persistence.connectors import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"))

    income = relationship("Income", back_populates="user")
    expenses = relationship("Expense", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)


class IncomeCategory(Base):
    __tablename__ = "income_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    income_description = Column(String, unique=True, nullable=False)

    incomes = relationship("Income", back_populates="income_type")


class Frequency(Base):
    __tablename__ = "frequencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    frequency_description = Column(String, unique=True, nullable=False)

    incomes = relationship("Income", back_populates="income_frequency")


class Income(Base):
    __tablename__ = "income"

    income_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    month = Column(Date, nullable=False)
    amount_encrypted = Column(String(255), nullable=False)
    income_type_id = Column(Integer, ForeignKey("income_categories.id"), nullable=False)
    income_frequency_id = Column(Integer, ForeignKey("frequencies.id"), nullable=False)

    user = relationship("User", back_populates="income")  
    income_type = relationship("IncomeCategory", back_populates="incomes")
    income_frequency = relationship("Frequency", back_populates="incomes")
    

class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    month = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("expense_categories.category_id"), nullable=False)
    sub_category_id = Column(Integer, ForeignKey("expense_sub_categories.sub_category_id"), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="expenses")
    expense_category = relationship("ExpenseCategory", back_populates="expenses")


class ExpenseCategory(Base):
    __tablename__ = "expense_categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), unique=True, nullable=False)
    category_description = Column(String(255), nullable=False)

    expenses = relationship("Expense", back_populates="expense_category")
    sub_categories = relationship("ExpenseSubCategory", back_populates="category")


class ExpenseSubCategory(Base):
    __tablename__ = "expense_sub_categories"

    sub_category_id = Column(Integer, primary_key=True, index=True)
    sub_category_name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("expense_categories.category_id"), nullable=False)

    category = relationship("ExpenseCategory", back_populates="sub_categories")  


class DashboardSetting(Base):
    __tablename__ = "dashboard_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chart_id = Column(Integer, nullable=False) 


class SavingsGoal(Base):
    __tablename__ = "savings_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_savings = Column(Float, nullable=False)