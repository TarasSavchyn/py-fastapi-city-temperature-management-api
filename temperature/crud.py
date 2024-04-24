from sqlalchemy.orm import Session

from temperature.models import TemperatureDB


def get_all_temperatures(db: Session):
    return db.query(TemperatureDB).all()
