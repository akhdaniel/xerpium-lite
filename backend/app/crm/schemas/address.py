from pydantic import BaseModel, validator
from typing import Optional
from backend.app.base.schemas.country import Country

class AddressBase(BaseModel):
    street: str
    city: str
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[Country] = None
    country_id: Optional[int] = None

    @validator('country_id', pre=True, always=True)
    def set_country_id_from_country(cls, v, values):
        if 'country' in values and values['country'] is not None:
            return values['country'].id
        return v

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    customer_id: int

    class Config:
        orm_mode = True
