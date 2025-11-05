from sqlalchemy.orm import Session
from backend.app.crm.models.address import Address
from backend.app.crm.schemas.address import AddressCreate, AddressUpdate

def get_address(db: Session, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Address).offset(skip).limit(limit).all()

def create_address(db: Session, address: AddressCreate, customer_id: int):
    db_address = Address(**address.dict(), customer_id=customer_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def update_address(db: Session, address_id: int, address: AddressUpdate):
    db_address = get_address(db, address_id)
    if db_address:
        for key, value in address.dict(exclude_unset=True).items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int):
    db_address = get_address(db, address_id)
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address
