from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.base.schemas.access_right import AccessRight, AccessRightCreate, AccessRightUpdate
from backend.app.base.services import access_right as access_right_service
from backend.app.database import get_db

router = APIRouter()

@router.post("/", response_model=AccessRight)
def create_access_right(access_right: AccessRightCreate, db: Session = Depends(get_db)):
    db_access_right = access_right_service.get_access_right_by_name(db, name=access_right.name)
    if db_access_right:
        raise HTTPException(status_code=400, detail="AccessRight already registered")
    return access_right_service.create_access_right(db=db, access_right=access_right)

@router.get("/", response_model=List[AccessRight])
def read_access_rights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    access_rights = access_right_service.get_access_rights(db, skip=skip, limit=limit)
    return access_rights

@router.get("/{access_right_id}", response_model=AccessRight)
def read_access_right(access_right_id: int, db: Session = Depends(get_db)):
    db_access_right = access_right_service.get_access_right(db, access_right_id=access_right_id)
    if db_access_right is None:
        raise HTTPException(status_code=404, detail="AccessRight not found")
    return db_access_right

@router.put("/{access_right_id}", response_model=AccessRight)
def update_access_right(access_right_id: int, access_right: AccessRightUpdate, db: Session = Depends(get_db)):
    db_access_right = access_right_service.update_access_right(db, access_right_id=access_right_id, access_right=access_right)
    if db_access_right is None:
        raise HTTPException(status_code=404, detail="AccessRight not found")
    return db_access_right

@router.delete("/{access_right_id}", response_model=AccessRight)
def delete_access_right(access_right_id: int, db: Session = Depends(get_db)):
    db_access_right = access_right_service.delete_access_right(db, access_right_id=access_right_id)
    if db_access_right is None:
        raise HTTPException(status_code=404, detail="AccessRight not found")
    return db_access_right
