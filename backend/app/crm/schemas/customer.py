from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from backend.app.base.schemas.country import Country

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    country_id: Optional[int] = None
    birth_date: Optional[date] = None
    last_contacted: Optional[datetime] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    country_id: Optional[int] = None
    birth_date: Optional[date] = None
    last_contacted: Optional[datetime] = None

class Customer(CustomerBase):
    id: int
    country: Optional[Country] = None

    class Config:
        from_attributes = True
