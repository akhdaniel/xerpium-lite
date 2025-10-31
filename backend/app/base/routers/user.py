from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.base.schemas.user import User, UserCreate, UserUpdate
from backend.app.base.schemas.user_group import UserGroup, UserGroupCreate
from backend.app.base.services import user as user_service
from backend.app.base.services import user_group as user_group_service
from backend.app.database import get_db
from backend.app.base.dependencies import has_permission, get_current_user

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/", response_model=User, dependencies=[Depends(has_permission("User", "create"))])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db=db, user=user)

@router.get("/", response_model=List[User], dependencies=[Depends(has_permission("User", "read"))])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User, dependencies=[Depends(has_permission("User", "read"))])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User, dependencies=[Depends(has_permission("User", "update"))])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_service.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=User, dependencies=[Depends(has_permission("User", "delete"))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/{user_id}/groups/", response_model=UserGroup, dependencies=[Depends(has_permission("UserGroup", "create"))])
def add_group_to_user(
    user_id: int,
    user_group: UserGroupCreate,
    db: Session = Depends(get_db)
):
    if user_group.user_id != user_id:
        raise HTTPException(status_code=400, detail="User ID in path and body do not match")
    db_user_group = user_group_service.get_user_group(
        db, user_id, user_group.group_id
    )
    if db_user_group:
        raise HTTPException(status_code=400, detail="User is already in this group")
    return user_group_service.create_user_group(db=db, user_group=user_group)

@router.delete("/{user_id}/groups/{group_id}", response_model=UserGroup, dependencies=[Depends(has_permission("UserGroup", "delete"))])
def remove_group_from_user(
    user_id: int,
    group_id: int,
    db: Session = Depends(get_db)
):
    db_user_group = user_group_service.delete_user_group(db, user_id, group_id)
    if db_user_group is None:
        raise HTTPException(status_code=404, detail="User group not found")
    return db_user_group
