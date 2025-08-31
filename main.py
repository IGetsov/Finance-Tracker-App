from fastapi import FastAPI
# import streamlit as st
# import pdb; pdb.set_trace()
from dotenv import load_dotenv
from api_routers.router_api_users import users_router
from api_routers.router_api_incomes import income_router

load_dotenv()

app = FastAPI()

# add API routers
app.include_router(users_router)
app.include_router(income_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000)
