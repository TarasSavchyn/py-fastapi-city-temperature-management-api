from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from temperature.crud import get_all_temperatures, update_temperatures_in_database
from temperature.schemas import Temperature

router = APIRouter()


@router.get("/temperatures/", response_model=List[Temperature])
def get_temperatures(db: Session = Depends(get_db)):
    return get_all_temperatures(db)


@router.post("/temperatures/update")
async def update_temperatures():
    await update_temperatures_in_database()
    return {"message": "Temperatures updated successfully"}
