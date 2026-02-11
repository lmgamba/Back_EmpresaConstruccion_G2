from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Construction(BaseModel):
    id_constructions: int
    name: str
    description: Optional[str] = None
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: str


class ConstructionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ConstructionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[str] = None
