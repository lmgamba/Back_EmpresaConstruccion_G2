from fastapi import APIRouter, Depends
from controllers import users_controllers
from models.users_models import User, UserCreate, UserUpdate
from core.dependencies import is_admin

router = APIRouter()

#Obtener usuario por ID
@router.get('/{user_id}', status_code=200)
async def get_user_id(user_id: str, user=Depends(is_admin)):
    return await users_controllers.get_user_id(int(user_id))

# Obtener todos los operarios
@router.get('/', status_code=200)
async def get_all_users(user=Depends(is_admin)):
    return await users_controllers.get_all_users()

# Crear operario
@router.post("/", status_code=201)
async def create_user(user: UserCreate, current_user=Depends(is_admin)):
    return await users_controllers.create_user(user)

#Actualizar operario
@router.put("/{user_id}", status_code=200)
async def update_user(user_id: str, user: UserUpdate, current_user= Depends(is_admin)):
    return await users_controllers.update_user(int(user_id), user)

#Eliminar operario
@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str, current_user=Depends(is_admin)):
    return await users_controllers.delete_user(int(user_id))