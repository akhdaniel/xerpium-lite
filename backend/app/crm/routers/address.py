from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.crm.schemas.address import Address, AddressCreate, AddressUpdate
from backend.app.crm.services import address as address_service
from backend.app.database import get_db

router = APIRouter()

@router.post("/", response_model=Address)
def create_address(address: AddressCreate, customer_id: int, db: Session = Depends(get_db)):
    return address_service.create_address(db=db, address=address, customer_id=customer_id)

@router.get("/", response_model=List[Address])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = address_service.get_addresses(db, skip=skip, limit=limit)
    return addresses

@router.get("/{address_id}", response_model=Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    db_address = address_service.get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@router.put("/{address_id}", response_model=Address)
def update_address(address_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    db_address = address_service.update_address(db, address_id=address_id, address=address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@router.delete("/{address_id}", response_model=Address)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = address_service.delete_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address
