from fastapi import APIRouter, Depends, Form, HTTPException
from services.income_service import delete_income, get_user_incomes, add_income, edit_income
from services.authentication_service import decode_access_token
from datetime import date



income_router = APIRouter(prefix='/api/income', tags=["Income"])

@income_router.get("/{user_id}")
def get_user_incomes(user_id: int):
    incomes = get_user_incomes(user_id)
    if not incomes:
        return None
    
    return incomes

@income_router.post("/{user_id}")
def create_income(
    user_id: int = Depends(decode_access_token),
    amount: float = Form(...),
    income_type: int = Form(...),
    frequency: int = Form(...)
    ):
    try:
        income = add_income(user_id, amount, income_type, frequency)
        return {"income": income}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@income_router.put("/{income_id}")
def update_income(
    income_id: int,
    amount: float = Form(...),
    income_type: int = Form(...),
    frequency: int = Form(...),
    month: date = Form(...),
    user_id: int = Depends(decode_access_token)
):
    try:
        income = edit_income(income_id, user_id, amount, income_type, frequency, month)
        return {"message": "Income updated successfully", "income": income}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@income_router.delete("/{income_id}")
def remove_income(
    income_id: int,
    user_id: int = Depends(decode_access_token)
):
    try:
        result = delete_income(income_id, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))