from fastapi import FastAPI
from services import get_place_from_api
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "travel_planner bd connected"}

@app.get("/test-api/{place_id}")
def test_api_connection(place_id: str):
    result = get_place_from_api(place_id)
    return result