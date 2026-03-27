from pydantic import BaseModel
from typing import Optional
from datetime import date


class PlaceBase(BaseModel):
    external_id: str
    notes: Optional[str] = None


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    is_visited: Optional[bool] = None


class PlaceResponse(PlaceBase):
    id: int
    project_id: int
    is_visited: bool

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    places: Optional[list[PlaceCreate]] = []


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectResponse(ProjectBase):
    id: int
    is_completed: bool # add status finish project

    class Config:
        from_attributes = True # these settings allow Pydantic to read data directly from the objects SQLAlchemy


