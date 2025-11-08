from pydantic import BaseModel
from typing import Optional
from .warehouse import Warehouse

class LocationBase(BaseModel):
    name: str
    warehouse_id: int

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = None
    warehouse_id: Optional[int] = None

class Location(LocationBase):
    id: int
    warehouse: Optional["Warehouse"] = None # Nested schema

    class Config:
        orm_mode = True

# Update forward refs for nested schemas
Location.update_forward_refs()
