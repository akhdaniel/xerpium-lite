from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True
