from pydantic.v1 import BaseModel


class City(BaseModel):
    id: int
    name: str
    additional_info: str = None

    class Config:
        orm_mode = True
