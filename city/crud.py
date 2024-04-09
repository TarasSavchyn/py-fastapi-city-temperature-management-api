from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from city.models import CityDB
from city.schemas import City
from dependencies import get_db
from main import app


@app.post("/cities/", response_model=City)
def create_city(city: City, db: Session = Depends(get_db)):
    db_city = CityDB(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@app.get("/cities/")
def get_cities(db: Session = Depends(get_db)):
    return db.query(CityDB).all()


@app.get("/cities/{city_id}", response_model=City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(CityDB).filter(CityDB.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=City)
def update_city(city_id: int, city: City, db: Session = Depends(get_db)):
    db_city = db.query(CityDB).filter(CityDB.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    for key, value in city.dict().items():
        setattr(db_city, key, value)
    db.commit()
    db.refresh(db_city)
    return db_city


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(CityDB).filter(CityDB.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"message": "City deleted successfully"}
