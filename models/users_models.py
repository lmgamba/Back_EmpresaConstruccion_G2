from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    surname: str
    mail: str
    password_hash: str
    role: str
    created_at: Optional[datetime] = None

class UserCreate(BaseModel):
    name: str
    surname: str
    mail: str
    password_hash: str
    role: str
    created_at: Optional[datetime] = None

class UserLogin(BaseModel):
    mail: str
    password_hash: str