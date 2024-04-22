from pydantic.v1 import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True
