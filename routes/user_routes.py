from http.client import HTTPException
from fastapi import APIRouter, Depends
from controllers import users_controllers
from models.users_models import User, UserCreate, UserUpdate
from core.dependencies import is_admin, get_current_user, is_admin_or_owner

router = APIRouter()

# ADMINISTRADOR OBTIENE USUARIO POR ID
@router.get('/{user_id}', status_code=200)
async def get_user_id(user_id: str, current_user = Depends(get_current_user)):
   
    # 1. SEGURIDAD: Comprobar si el que pide es Admin o es el propio usuario
    # Usamos int() en ambos lados para evitar el error de Texto vs Número
    if current_user['role'] != 'admin' and int(current_user['id_users']) != int(user_id):
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este perfil")
    return await users_controllers.get_user_id(int(user_id))

# ADMINISTRADOR OBTIENE TODOS LOS OPERARIOS
@router.get('/', status_code=200)
async def get_all_users(user=Depends(is_admin)):
    return await users_controllers.get_all_users()

# ADMINISTRADOR CREA UNA CUENTA DE OPERARIO
@router.post("/", status_code=201)
async def create_user(user: UserCreate):
    return await users_controllers.create_user(user)

# ADMINISTRADOR ACTUALIZA UNA CUENTA DE OPERARIO
@router.put("/{user_id}", status_code=200)
async def update_user(user_id: str, user: UserUpdate, current_user = Depends(get_current_user)):
   
    # 1. SEGURIDAD: Comprobar si el que pide es Admin o es el propio usuario
    # Usamos int() en ambos lados para evitar el error de Texto vs Número
    if current_user['role'] != 'admin' and int(current_user['id_users']) != int(user_id):
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este perfil")
    return await users_controllers.update_user(int(user_id), user)

#TODO: ADMINISTRADOR DESACTIVA UNA CUENTA DE OPERARIO
# @router.patch("/{user_id}", status_code=200)
# async def deactivate_user(user_id: str, status: bool, user_admin= Depends(is_admin)):
#     return await users_controllers.deactivate_user(int(user_id), status)

# ADMINISTRADOR BORRA UNA CUENTA DE OPERARIO
@router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: str, user= Depends(is_admin)):
    return await users_controllers.delete_user(int(user_id))

# ENCONTRAR USUARIO POR CORREO
@router.get('/mail/{mail}', status_code=200)
async def search_mail(mail: str):
    return await users_controllers.search_mail(mail)
