from typing import Type

import aiohttp
from sqlalchemy.orm import Session

from temperature.models import TemperatureDB
from city.models import CityDB


async def fetch_temperature(city: CityDB) -> dict:
    async with aiohttp.ClientSession() as session:
        url = (
            f"http://api.openweathermap.org/data/2.5/weather?q="
            f"{city.name}&appid=your_api_key&units=metric"
        )
        async with session.get(url) as response:
            data = await response.json()
            if "main" in data and "temp" in data["main"]:
                temperature = data["main"]["temp"]
                return {"city_id": city.id, "temperature": temperature}
            else:
                return {"city_id": city.id, "temperature": None}


def create_temperature(db: Session, temperature: dict) -> None:
    db_temperature = TemperatureDB(**temperature)
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)


async def update_temperatures_in_database(db: Session) -> None:
    cities = db.query(CityDB).all()
    for city in cities:
        temperature_data = await fetch_temperature(city)
        create_temperature(db, temperature_data)


def get_all_temperatures(db: Session) -> list[Type[TemperatureDB]]:
    return db.query(TemperatureDB).all()


def get_temperatures_by_city(city_id: int, db: Session) -> list[TemperatureDB]:
    return db.query(
        TemperatureDB
    ).filter(
        TemperatureDB.city_id == city_id
    ).all()
