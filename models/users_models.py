from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    surname: str
    mail: str
    password: str
    role: str
    created_at: Optional[datetime] = None

class UserCreate(BaseModel):
    name: str
    surname: str
    mail: str
    password: str
    role: str
    created_at: Optional[datetime] = None

class UserLogin(BaseModel):
    mail: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    mail: str
    role: str
    created_at: Optional[datetime] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    mail: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[datetime] = None