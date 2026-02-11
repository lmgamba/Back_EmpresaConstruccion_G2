from fastapi import APIRouter, Depends
from controllers import users_controllers
from models.users_models import User
from core.dependencies import is_admin_or_owner

router = APIRouter()

#Obtener usuario por ID
@router.get('/{user_id}', status_code=200)
async def get_user_id(user_id: str, user=Depends(is_admin_or_owner)):
    return await users_controllers.get_user_id(int(user_id))

# Obtener todos los operarios
@router.get('/', status_code=200)
async def get_all_users(user=Depends(is_admin_or_owner)):
    return await users_controllers.get_all_users()