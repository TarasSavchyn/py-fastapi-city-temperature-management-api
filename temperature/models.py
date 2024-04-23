from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from city.models import Base, CityDB


class TemperatureDB(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    temperature = Column(Float)
    date_time = Column(DateTime)

    city = relationship("CityDB", back_populates="temperatures")
