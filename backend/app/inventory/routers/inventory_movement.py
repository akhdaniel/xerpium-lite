from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.inventory.schemas.inventory_movement import InventoryMovement, InventoryMovementCreate, InventoryMovementUpdate
from backend.app.inventory.services import inventory_movement as inventory_movement_service

router = APIRouter()

@router.post("/", response_model=InventoryMovement)
def create_inventory_movement_endpoint(movement: InventoryMovementCreate, db: Session = Depends(get_db)):
    return inventory_movement_service.create_inventory_movement(db=db, movement=movement)

@router.get("/", response_model=List[InventoryMovement])
def read_inventory_movements_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movements = inventory_movement_service.get_inventory_movements(db, skip=skip, limit=limit)
    return movements

@router.get("/{movement_id}", response_model=InventoryMovement)
def read_inventory_movement_endpoint(movement_id: int, db: Session = Depends(get_db)):
    db_movement = inventory_movement_service.get_inventory_movement(db, movement_id=movement_id)
    if db_movement is None:
        raise HTTPException(status_code=404, detail="Inventory Movement not found")
    return db_movement

@router.put("/{movement_id}", response_model=InventoryMovement)
def update_inventory_movement_endpoint(movement_id: int, movement: InventoryMovementUpdate, db: Session = Depends(get_db)):
    db_movement = inventory_movement_service.update_inventory_movement(db, movement_id=movement_id, movement=movement)
    if db_movement is None:
        raise HTTPException(status_code=404, detail="Inventory Movement not found")
    return db_movement

@router.delete("/{movement_id}", response_model=InventoryMovement)
def delete_inventory_movement_endpoint(movement_id: int, db: Session = Depends(get_db)):
    db_movement = inventory_movement_service.delete_inventory_movement(db, movement_id=movement_id)
    if db_movement is None:
        raise HTTPException(status_code=404, detail="Inventory Movement not found")
    return db_movement
