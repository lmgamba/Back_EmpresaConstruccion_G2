from fastapi import APIRouter, Depends, HTTPException
from controllers import assignments_controllers
from models.assignments_models import AssignmentCreate
from core.dependencies import is_admin, get_current_user

router = APIRouter()

# Crear asignación (solo admin)
@router.post("/", status_code=201)
async def create_assignment(assignment: AssignmentCreate, current_user=Depends(is_admin)):
    return await assignments_controllers.create_assignment(assignment)



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
    return await assignments_controllers.finish_assignment(assignment_id)
