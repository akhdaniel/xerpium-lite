from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from backend.app.crm.schemas.address import Address, AddressCreate

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    birth_date: Optional[date] = None
    last_contacted: Optional[datetime] = None

class CustomerCreate(CustomerBase):
    addresses: List[AddressCreate] = []

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birth_date: Optional[date] = None
    last_contacted: Optional[datetime] = None
    addresses: List[AddressCreate] = []

class Customer(CustomerBase):
    id: int
    addresses: List[Address] = []

    class Config:
        from_attributes = True
