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
    project_data = project.model_dump(exclude={"places"})
    db_project = models.Project(**project_data)
    db.add(db_project)
    db.commit()
    db.refresh(db_project) # upd for recieve generated ID

    if project.places:
        for p_data in project.places:
            api_res = get_place_from_api(p_data.external_id)
            if api_res["exists"]:
                new_place = models.Place(**p_data.model_dump(), project_id=db_project.id)
                db.add(new_place)
        db.commit()
        db.refresh(db_project)

    return db_project


@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return db_project


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    for place in db_project.places:
        if place.is_visited:
            raise HTTPException(
                status_code=400, detail="Cannot delete project - some place is already visited"
            )

    db.delete(db_project)
    db.commit()

    return {"message": "Project deleted"}


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


@app.get("/projects/{project_id}/places/", response_model=List[schemas.PlaceResponse])
def get_places_for_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    return db_project.places


@app.get ("/projects/{project_id}/places/{place_id}/", response_model=schemas.PlaceResponse)
def get_place(project_id: int, place_id: int, db: Session = Depends(get_db)):
    db_place = db.query(models.Place).filter(
        models.Place.id == place_id,
        models.Place.project_id == project_id
    ).first()

    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")

    return db_place


@app.put("/projects/{project_id}/places/{place_id}/", response_model=schemas.PlaceResponse)
def update_place(project_id: int, place_id: int, place_update: schemas.PlaceUpdate, db: Session = Depends(get_db)):
    db_place = db.query(models.Place).filter(
        models.Place.id == place_id,
        models.Place.project_id == project_id
    ).first()

    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")

    update_data = place_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_place, key, value)

    db.commit()
    db.refresh(db_place)

    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    all_visited = all(p.is_visited for p in db_project.places)
    if all_visited and len(db_project.places) > 0:
        db_project.is_completed = True
    else:
        db_project.is_completed = False

    db.commit()
    return db_place