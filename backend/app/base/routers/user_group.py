from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.base.schemas.user_group import UserGroup, UserGroupCreate
from backend.app.base.services import user_group as user_group_service
from backend.app.database import get_db

router = APIRouter()

@router.post("/", response_model=UserGroup)
def create_user_group(user_group: UserGroupCreate, db: Session = Depends(get_db)):
    db_user_group = user_group_service.get_user_group(
        db, user_group.user_id, user_group.group_id
    )
    if db_user_group:
        raise HTTPException(status_code=400, detail="User group already exists")
    return user_group_service.create_user_group(db=db, user_group=user_group)

@router.get("/user/{user_id}", response_model=List[UserGroup])
def read_user_groups_by_user(user_id: int, db: Session = Depends(get_db)):
    user_groups = user_group_service.get_user_groups_by_user(db, user_id)
    return user_groups

@router.delete("/{user_id}/{group_id}", response_model=UserGroup)
def delete_user_group(user_id: int, group_id: int, db: Session = Depends(get_db)):
    db_user_group = user_group_service.delete_user_group(db, user_id, group_id)
    if db_user_group is None:
        raise HTTPException(status_code=404, detail="User group not found")
    return db_user_group
