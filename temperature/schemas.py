from typing import Optional

from pydantic import BaseModel

from city.schemas import City


class TemperatureBase(BaseModel):
    temperature: float
    date_time: str


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city_id: Optional[int]
    city: Optional[City]

    class Config:
        orm_mode = True
