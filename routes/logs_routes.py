from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from controllers import logs_controllers
from models.logs_models import LogCreate
from core.dependencies import get_current_user, is_admin

router = APIRouter()

# CREAR LOG (crearla el operario asignado a la obra)
@router.post("/", status_code=201)
async def create_log(log : LogCreate, background_tasks: BackgroundTasks, current_user=Depends(get_current_user)):
    return await logs_controllers.create_log(current_user["id_users"], log, background_tasks)


# LISTAR LOGS POR OBRA (admin)
@router.get("/construction/{construction_id}", status_code=200)
async def get_logs_by_construction(construction_id: int, current_user=Depends(get_current_user)):
    return await logs_controllers.get_logs_by_construction(construction_id, current_user)

# LISTAR LOGS POR USUARIO (admin)
@router.get("/user/{user_id}", status_code=200)
async def get_logs_by_user(user_id :int, current_user=Depends(get_current_user)):
    # 1. Verificamos si es Admin
    is_admin = current_user.get("role") == "admin"
    
    # 2. Verificamos si el ID solicitado es el del propio usuario logueado
    is_owner = current_user.get("id_users") == user_id

    # Si no es ninguna de las dos, lanzamos error 403 (Prohibido)
    if not (is_admin or is_owner):
        raise HTTPException(
            status_code=403, 
            detail="No tienes permiso para ver los logs de otro usuario."
        )

    # Si pasó la validación, llamamos al controlador
    return await logs_controllers.get_logs_by_user(user_id)