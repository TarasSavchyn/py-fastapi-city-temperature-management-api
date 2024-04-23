from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from city.crud import get_all_cities, create_new_city
from city.schemas import City, CityCreate
from dependencies import get_db



app = FastAPI()



@app.get("/cities/", response_model=List[City])
def get_cities(db: Session = Depends(get_db)):
    return get_all_cities(db)


@app.post("/cities/")
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return create_new_city(db=db, city=city)

