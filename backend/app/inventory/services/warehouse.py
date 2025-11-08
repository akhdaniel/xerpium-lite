from sqlalchemy.orm import Session
from backend.app.inventory.models.warehouse import Warehouse
from backend.app.inventory.schemas.warehouse import WarehouseCreate, WarehouseUpdate

def get_warehouse(db: Session, warehouse_id: int):
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

def get_warehouse_by_name(db: Session, name: str):
    return db.query(Warehouse).filter(Warehouse.name == name).first()

def get_warehouses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Warehouse).offset(skip).limit(limit).all()

def create_warehouse(db: Session, warehouse: WarehouseCreate):
    db_warehouse = Warehouse(**warehouse.dict())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

def update_warehouse(db: Session, warehouse_id: int, warehouse: WarehouseUpdate):
    db_warehouse = get_warehouse(db, warehouse_id)
    if db_warehouse:
        update_data = warehouse.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_warehouse, key, value)
        db.commit()
        db.refresh(db_warehouse)
    return db_warehouse

def delete_warehouse(db: Session, warehouse_id: int):
    db_warehouse = get_warehouse(db, warehouse_id)
    if db_warehouse:
        db.delete(db_warehouse)
        db.commit()
    return db_warehouse
