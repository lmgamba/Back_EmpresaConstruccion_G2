from fastapi import APIRouter, Depends, Query
from controllers import constructions_controllers
from models.constructions_models import ConstructionCreate, ConstructionUpdate
from core.dependencies import is_admin

router = APIRouter()

@router.get("/")
async def get_all(status: str = Query(None), current_user=Depends(is_admin)):
    return await constructions_controllers.get_all_constructions(status)

@router.post("/", status_code=201)
async def create(construction: ConstructionCreate, current_user=Depends(is_admin)):
    return await constructions_controllers.create_construction(construction)

@router.put("/{construction_id}")
async def update(construction_id: int, construction: ConstructionUpdate, current_user=Depends(is_admin)):
    return await constructions_controllers.update_construction(construction_id, construction)

@router.delete("/{construction_id}", status_code=204)
async def delete(construction_id: int, current_user=Depends(is_admin)):
    return await constructions_controllers.delete_construction(construction_id)

@router.get("/{construction_id}/workers", status_code=200)
async def get_workers(construction_id: int, current_user=Depends(is_admin)):
    return await constructions_controllers.get_workers_by_construction(construction_id)
