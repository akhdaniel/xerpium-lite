from pydantic import BaseModel
from typing import Optional

class CountryBase(BaseModel):
    name: str

class CountryCreate(CountryBase):
    pass

class CountryUpdate(CountryBase):
    pass

class Country(CountryBase):
    id: int

    class Config:
        from_attributes = True
