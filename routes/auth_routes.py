from fastapi import APIRouter
from models.users_models import UserCreate, UserLogin
from controllers import auth_controllers

router = APIRouter()

# registro de usuario
@router.post("/register", status_code=201)
async def register_user(user: UserCreate):
    return await auth_controllers.register_user(user)

# login de usuario
@router.post('/login', status_code=200)
async def login_user(user_login: UserLogin):
    return await auth_controllers.login_user(user_login)