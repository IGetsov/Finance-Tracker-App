from fastapi import APIRouter
from services import income_service as inc


income_router = APIRouter(prefix='/api/income', tags=["Income"])

@income_router.get("/{user_id}")
def get_user_incomes(user_id: int):
    incomes = inc.get_user_incomes(user_id)
    if not incomes:
        return None
    
    return incomes