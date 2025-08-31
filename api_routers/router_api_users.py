from fastapi import APIRouter, Form, Response
from services import user_service as us

users_router = APIRouter(prefix='/api/users', tags=["Users"])

@users_router.get("/")
def get_all_users_route():
    users = us.view_users()

    if not users:
        return None
    
    return users


@users_router.get("/roles")
def get_user_roles():
    roles = us.view_roles()
    if not roles:
        return None
    
    return roles


@users_router.post("/register")
def register_user(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    return us.register_user(username, email, password)


@users_router.post("/login")
def login_user(username: str = Form(...), password: str = Form(...)):
    return us.login_user(username, password)


@users_router.post("/logout")
def logout_user(response: Response):
    # You can optionally clear cookies if you stored token there
    response.delete_cookie(key="session_id")
    return {"detail": "Logout successful. Please discard token on client."}