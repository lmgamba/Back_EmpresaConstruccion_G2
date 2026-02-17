from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from controllers import assignments_controllers
from models.assignments_models import AssignmentCreate
from core.dependencies import is_admin, get_current_user

router = APIRouter()


# Crear asignación (solo admin)
@router.post("/", status_code=201)
async def create_assignment(
    assignment: AssignmentCreate,
    background_tasks: BackgroundTasks,
    current_user=Depends(is_admin),
):
    # Pasamos el objeto assignment Y el objeto background_tasks al controlador
    return await assignments_controllers.create_assignment(assignment, background_tasks)


# Obtener todas las asignaciones (solo admin)
@router.get("/", status_code=200)
async def get_all_assignments(current_user=Depends(is_admin)):
    return await assignments_controllers.get_all_assignments()


# Ver asignaciones de un usuario (admin o el propio usuario)
@router.get("/user/{user_id}", status_code=200)
async def get_assignments_by_user(user_id: int, current_user=Depends(get_current_user)):
    # Si es admin puede ver cualquiera
    if current_user["role"] == "admin":
        return await assignments_controllers.get_assignments_by_user(user_id)
    # Si es operario solo puede ver las suyas
    if current_user["id_users"] == user_id:
        return await assignments_controllers.get_assignments_by_user(user_id)
    raise HTTPException(status_code=403, detail="No tienes permisos")


# Finalizar asignación (solo admin)
@router.put("/{assignment_id}/finish", status_code=200)
async def finish_assignment(assignment_id: int, current_user=Depends(is_admin)):
    print(assignment_id)
    return await assignments_controllers.finish_assignment(assignment_id)
