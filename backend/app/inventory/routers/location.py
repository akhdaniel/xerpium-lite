from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.inventory.schemas.location import Location, LocationCreate, LocationUpdate
from backend.app.inventory.services import location as location_service

router = APIRouter()

@router.post("/", response_model=Location)
def create_location_endpoint(location: LocationCreate, db: Session = Depends(get_db)):
    return location_service.create_location(db=db, location=location)

@router.get("/", response_model=List[Location])
def read_locations_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    locations = location_service.get_locations(db, skip=skip, limit=limit)
    return locations

@router.get("/by_warehouse/{warehouse_id}", response_model=List[Location])
def read_locations_by_warehouse_endpoint(warehouse_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    locations = location_service.get_locations_by_warehouse(db, warehouse_id=warehouse_id, skip=skip, limit=limit)
    return locations

@router.get("/{location_id}", response_model=Location)
def read_location_endpoint(location_id: int, db: Session = Depends(get_db)):
    db_location = location_service.get_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@router.put("/{location_id}", response_model=Location)
def update_location_endpoint(location_id: int, location: LocationUpdate, db: Session = Depends(get_db)):
    db_location = location_service.update_location(db, location_id=location_id, location=location)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@router.delete("/{location_id}", response_model=Location)
def delete_location_endpoint(location_id: int, db: Session = Depends(get_db)):
    db_location = location_service.delete_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location
