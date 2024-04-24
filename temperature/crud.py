import asyncio

import aiohttp
from sqlalchemy.orm import Session

from city.models import CityDB
from database import SessionLocal
from temperature.models import TemperatureDB


def get_all_temperatures(db: Session):
    return db.query(TemperatureDB).all()


async def fetch_temperature(city: CityDB):
    async with aiohttp.ClientSession() as session:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid=your_api_key&units=metric"
        async with session.get(url) as response:
            data = await response.json()
            temperature = data["main"]["temp"]
            return {"city_id": city.id, "temperature": temperature}


async def update_temperatures_in_database():
    async with SessionLocal() as session:
        cities = session.query(CityDB).all()
        tasks = [fetch_temperature(city) for city in cities]
        temperatures = await asyncio.gather(*tasks)
        for temp_data in temperatures:
            temperature = TemperatureDB(**temp_data)
            session.add(temperature)
        session.commit()
