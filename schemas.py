from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True # these settings allow Pydantic to read data directly from the objects SQLAlchemy
