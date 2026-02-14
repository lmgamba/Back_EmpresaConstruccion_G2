from fastapi import APIRouter, BackgroundTasks, Depends
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
async def get_logs_by_construction(construction_id: int, current_user=Depends(is_admin)):
    return await logs_controllers.get_logs_by_construction(construction_id)

# LISTAR LOGS POR USUARIO (admin)
@router.get("/user/{user_id}", status_code=200)
async def get_logs_by_user(user_id :int, current_user=Depends(is_admin)):
    return await logs_controllers.get_logs_by_user(user_id)