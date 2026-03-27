from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from services import get_place_from_api
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "travel_planner bd connected"}


@app.get("/test-api/{place_id}")
def test_api_connection(place_id: str):
    result = get_place_from_api(place_id)
    return result

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/projects/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(**project.model_dump())

    db.add(db_project)
    db.commit()
    db.refresh(db_project) # upd for recieve generated ID

    return db_project


@app.get("/projects/", response_model=List[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    return projects


@app.post("/projects/{project_id}/places/", response_model=schemas.PlaceResponse)
def add_place_to_project(project_id: int, place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project: # check project
        raise HTTPException(status_code=404, detail="Project not found")

    if len(db_project.places) >= 10: # check limits
        raise HTTPException(status_code=400, detail="Already have 10 places")

    for existing_place in db_project.places: #check places in project
        if existing_place.external_id == place.external_id:
            raise HTTPException(status_code=400, detail="Place already exists")

    api_result = get_place_from_api(place.external_id)
    if not api_result["exists"]: # call to our external API
        raise HTTPException(status_code=404, detail="Place not found in API external")

    db_place = models.Place(
        project_id=project_id,
        external_id=place.external_id,
        notes=place.notes
    )

    db.add(db_place)
    db.commit()
    db.refresh(db_place)

    return db_place

