from sqlalchemy.orm import Session

from city.models import CityDB
from city.schemas import CityCreate


def get_all_cities(db: Session, ):
    return db.query(CityDB).all()


def create_new_city(db: Session, city: CityCreate):
    db_city = CityDB(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city
