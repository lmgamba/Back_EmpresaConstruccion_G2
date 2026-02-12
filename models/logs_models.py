from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogCreate(BaseModel):
    description: str
    type: str 
    constructionsSites_id: int

class LogResponse(BaseModel):
    id_logs: int
    description: str
    type: str
    date_register: Optional[datetime]
    users_id: int
    constructionsSites_id: int