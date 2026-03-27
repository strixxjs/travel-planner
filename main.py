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