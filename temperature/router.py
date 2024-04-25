import asyncio
from typing import List, Type

import aiohttp
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from temperature.crud import (
    get_all_temperatures,
    get_temperatures_by_city,
    update_temperature,
)
from temperature.models import TemperatureDB
from temperature.schemas import Temperature

router = APIRouter()


@router.get("/temperatures/", response_model=List[Temperature])
def get_temperatures(
        db: Session = Depends(get_db)
) -> list[Type[TemperatureDB]]:
    return get_all_temperatures(db)


@router.get("/temperatures/{city_id}", response_model=list[Temperature])
def get_temperatures_by_city_id(
    city_id: int, db: Session = Depends(get_db)
) -> List[TemperatureDB]:
    temperatures = get_temperatures_by_city(city_id, db)
    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperatures not found")
    return temperatures


@router.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)) -> dict:
    temperatures = db.query(TemperatureDB).all()
    if not temperatures:
        raise HTTPException(status_code=404, detail="Температури не знайдені")

    async with aiohttp.ClientSession() as session:
        tasks = []
        for temperature in temperatures:
            tasks.append(update_temperature(session, db, temperature))
        await asyncio.gather(*tasks)

    return {"success": True}
