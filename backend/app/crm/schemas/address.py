from pydantic import BaseModel, validator
from typing import Optional
from backend.app.base.schemas.country import Country

class AddressBase(BaseModel):
    street: str
    city: str
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country_id: int

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    customer_id: int
    country: Optional[Country] = None

    class Config:
        orm_mode = True
