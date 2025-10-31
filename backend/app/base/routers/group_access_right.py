from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.base.schemas.group_access_right import GroupAccessRight, GroupAccessRightCreate
from backend.app.base.services import group_access_right as group_access_right_service
from backend.app.database import get_db

router = APIRouter()

@router.post("/", response_model=GroupAccessRight)
def create_group_access_right(group_access_right: GroupAccessRightCreate, db: Session = Depends(get_db)):
    db_group_access_right = group_access_right_service.get_group_access_right(
        db, group_access_right.group_id, group_access_right.access_right_id
    )
    if db_group_access_right:
        raise HTTPException(status_code=400, detail="Group access right already exists")
    return group_access_right_service.create_group_access_right(db=db, group_access_right=group_access_right)

@router.get("/group/{group_id}", response_model=List[GroupAccessRight])
def read_group_access_rights_by_group(group_id: int, db: Session = Depends(get_db)):
    group_access_rights = group_access_right_service.get_group_access_rights_by_group(db, group_id)
    return group_access_rights

@router.delete("/{group_id}/{access_right_id}", response_model=GroupAccessRight)
def delete_group_access_right(group_id: int, access_right_id: int, db: Session = Depends(get_db)):
    db_group_access_right = group_access_right_service.delete_group_access_right(db, group_id, access_right_id)
    if db_group_access_right is None:
        raise HTTPException(status_code=404, detail="Group access right not found")
    return db_group_access_right
