from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.inventory.schemas.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate
from backend.app.inventory.services import warehouse as warehouse_service

router = APIRouter()

@router.post("/", response_model=Warehouse)
def create_warehouse_endpoint(warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    db_warehouse = warehouse_service.get_warehouse_by_name(db, name=warehouse.name)
    if db_warehouse:
        raise HTTPException(status_code=400, detail="Warehouse name already registered")
    return warehouse_service.create_warehouse(db=db, warehouse=warehouse)

@router.get("/", response_model=List[Warehouse])
def read_warehouses_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    warehouses = warehouse_service.get_warehouses(db, skip=skip, limit=limit)
    return warehouses

@router.get("/{warehouse_id}", response_model=Warehouse)
def read_warehouse_endpoint(warehouse_id: int, db: Session = Depends(get_db)):
    db_warehouse = warehouse_service.get_warehouse(db, warehouse_id=warehouse_id)
    if db_warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return db_warehouse

@router.put("/{warehouse_id}", response_model=Warehouse)
def update_warehouse_endpoint(warehouse_id: int, warehouse: WarehouseUpdate, db: Session = Depends(get_db)):
    db_warehouse = warehouse_service.update_warehouse(db, warehouse_id=warehouse_id, warehouse=warehouse)
    if db_warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return db_warehouse

@router.delete("/{warehouse_id}", response_model=Warehouse)
def delete_warehouse_endpoint(warehouse_id: int, db: Session = Depends(get_db)):
    db_warehouse = warehouse_service.delete_warehouse(db, warehouse_id=warehouse_id)
    if db_warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return db_warehouse
