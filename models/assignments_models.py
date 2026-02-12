from pydantic import BaseModel
from typing import Optional
from datetime import date

class AssignmentCreate(BaseModel):
    users_id: int
    constructionsSites_id: int
    date_start: date
    date_finish: Optional[date] = None
