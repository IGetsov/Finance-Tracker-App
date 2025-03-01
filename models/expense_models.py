from pydantic import BaseModel, Field
from datetime import date


class ExpenseCreate(BaseModel):
    user_id: int = Field(gt=0, description="User ID must be greater than 0")
    month: date
    amount: float = Field(gt=0, description="Income amount must be greater than 0")
    expense_type: int
    description: str