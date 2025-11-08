from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .product import Product
from .location import Location

class InventoryMovementBase(BaseModel):
    product_id: int
    source_location_id: Optional[int] = None
    destination_location_id: int
    quantity: float

class InventoryMovementCreate(InventoryMovementBase):
    pass

class InventoryMovementUpdate(BaseModel):
    product_id: Optional[int] = None
    source_location_id: Optional[int] = None
    destination_location_id: Optional[int] = None
    quantity: Optional[float] = None

class InventoryMovement(InventoryMovementBase):
    id: int
    movement_date: datetime
    product: Optional["Product"] = None # Nested schema
    source_location: Optional["Location"] = None # Nested schema
    destination_location: Optional["Location"] = None # Nested schema

    class Config:
        orm_mode = True

# Update forward refs for nested schemas
InventoryMovement.update_forward_refs()
