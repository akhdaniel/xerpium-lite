from sqlalchemy.orm import Session
from backend.app.inventory.models.inventory_movement import InventoryMovement
from backend.app.inventory.schemas.inventory_movement import InventoryMovementCreate, InventoryMovementUpdate

def get_inventory_movement(db: Session, movement_id: int):
    return db.query(InventoryMovement).filter(InventoryMovement.id == movement_id).first()

def get_inventory_movements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(InventoryMovement).offset(skip).limit(limit).all()

def create_inventory_movement(db: Session, movement: InventoryMovementCreate):
    db_movement = InventoryMovement(**movement.dict())
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

def update_inventory_movement(db: Session, movement_id: int, movement: InventoryMovementUpdate):
    db_movement = get_inventory_movement(db, movement_id)
    if db_movement:
        update_data = movement.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_movement, key, value)
        db.commit()
        db.refresh(db_movement)
    return db_movement

def delete_inventory_movement(db: Session, movement_id: int):
    db_movement = get_inventory_movement(db, movement_id)
    if db_movement:
        db.delete(db_movement)
        db.commit()
    return db_movement
