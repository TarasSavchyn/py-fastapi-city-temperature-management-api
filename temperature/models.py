from sqlalchemy import Column, Integer

from database import TemperatureBase


class TemperatureDB(TemperatureBase):
    __tablename__ = "temperatures"
    id = Column(Integer, primary_key=True, index=True)

