from pydantic import BaseModel
from typing import Optional

class WarehouseBase(BaseModel):
    name: str
    address: Optional[str] = None

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

class Warehouse(WarehouseBase):
    id: int

    class Config:
        orm_mode = True
