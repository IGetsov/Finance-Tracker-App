from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from persistence.connectors import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"))

    # income = relationship("Income", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)


# class Income(Base):
#     __tablename__ = "income"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     month = Column(Date, nullable=False)
#     amount = Column(Float, nullable=False)

#     user = relationship("User", back_populates="income")


# class Expense(Base):
#     __tablename__ = "expenses"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     amount = Column(Float, nullable=False)
#     category_id = Column(Integer, ForeignKey("expense_categories.id"), nullable=False)
#     date_time = Column(DateTime, nullable=False)
#     source = Column(String(50), nullable=True)  # "manual", "csv_upload", "qr_scan"

#     user = relationship("User", back_populates="expenses")
#     category = relationship("ExpenseCategory")


# class ExpenseCategory(Base):
#     __tablename__ = "expense_categories"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), unique=True, nullable=False)


# class DashboardSetting(Base):
#     __tablename__ = "dashboard_settings"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     chart_id = Column(Integer, nullable=False) 


# class SavingsGoal(Base):
#     __tablename__ = "savings_goals"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     target_amount = Column(Float, nullable=False)
#     current_savings = Column(Float, nullable=False)