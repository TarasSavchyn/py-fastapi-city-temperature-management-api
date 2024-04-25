from datetime import datetime
from typing import Type, Optional
from sqlalchemy.orm import Session

from temperature.models import TemperatureDB


def get_all_temperatures(db: Session) -> list[Type[TemperatureDB]]:
    return db.query(TemperatureDB).all()


def get_temperatures_by_city(city_id: int, db: Session) -> list[TemperatureDB]:
    return db.query(TemperatureDB).filter(
        TemperatureDB.city_id == city_id
    ).all()


async def update_temperature(
        session: Session,
        db: Session,
        temperature: TemperatureDB
) -> None:
    city_name = temperature.city.name
    temperature_str = await get_online_temperature_by_city(session, city_name)
    if temperature_str is not None:
        temperature.temperature = float(temperature_str)
        temperature.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.commit()


async def get_online_temperature_by_city(
        session: Session, city_name: str,
) -> Optional[float]:
    url = f"https://wttr.in/{city_name}?format=%t"
    async with session.get(url) as response:
        if response.status == 200:
            temperature_str = await response.text()
            try:
                temperature = float(temperature_str[:-2])
                return temperature
            except ValueError:
                return None
    return None
