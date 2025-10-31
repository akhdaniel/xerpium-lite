from sqlalchemy.orm import Session
from backend.app.base.models.access_right import AccessRight
from backend.app.base.schemas.access_right import AccessRightCreate, AccessRightUpdate

def get_access_right(db: Session, access_right_id: int):
    return db.query(AccessRight).filter(AccessRight.id == access_right_id).first()

def get_access_right_by_name(db: Session, name: str):
    return db.query(AccessRight).filter(AccessRight.name == name).first()

def get_access_rights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AccessRight).offset(skip).limit(limit).all()

def create_access_right(db: Session, access_right: AccessRightCreate):
    db_access_right = AccessRight(name=access_right.name, description=access_right.description)
    db.add(db_access_right)
    db.commit()
    db.refresh(db_access_right)
    return db_access_right

def update_access_right(db: Session, access_right_id: int, access_right: AccessRightUpdate):
    db_access_right = get_access_right(db, access_right_id)
    if not db_access_right:
        return None
    access_right_data = access_right.dict(exclude_unset=True)
    for key, value in access_right_data.items():
        setattr(db_access_right, key, value)
    db.add(db_access_right)
    db.commit()
    db.refresh(db_access_right)
    return db_access_right

def delete_access_right(db: Session, access_right_id: int):
    db_access_right = get_access_right(db, access_right_id)
    if not db_access_right:
        return None
    db.delete(db_access_right)
    db.commit()
    return db_access_right
