from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.base.schemas.group import Group, GroupCreate, GroupUpdate
from backend.app.base.schemas.group_access_right import GroupAccessRight, GroupAccessRightCreate
from backend.app.base.schemas.group_menu import GroupMenu, GroupMenuCreate
from backend.app.base.services import group as group_service
from backend.app.base.services import group_access_right as group_access_right_service
from backend.app.base.services import group_menu as group_menu_service
from backend.app.database import get_db

router = APIRouter()

@router.post("/", response_model=Group)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    db_group = group_service.get_group_by_name(db, name=group.name)
    if db_group:
        raise HTTPException(status_code=400, detail="Group already registered")
    return group_service.create_group(db=db, group=group)

@router.get("/", response_model=List[Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = group_service.get_groups(db, skip=skip, limit=limit)
    return groups

@router.get("/{group_id}", response_model=Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = group_service.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.put("/{group_id}", response_model=Group)
def update_group(group_id: int, group: GroupUpdate, db: Session = Depends(get_db)):
    db_group = group_service.update_group(db, group_id=group_id, group=group)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.delete("/{group_id}", response_model=Group)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    db_group = group_service.delete_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.post("/{group_id}/access_rights/", response_model=GroupAccessRight)
def add_access_right_to_group(
    group_id: int,
    access_right: GroupAccessRightCreate,
    db: Session = Depends(get_db)
):
    if access_right.group_id != group_id:
        raise HTTPException(status_code=400, detail="Group ID in path and body do not match")
    db_group_access_right = group_access_right_service.get_group_access_right(
        db, group_id, access_right.access_right_id
    )
    if db_group_access_right:
        raise HTTPException(status_code=400, detail="Group access right already exists")
    return group_access_right_service.create_group_access_right(db=db, group_access_right=access_right)

@router.delete("/{group_id}/access_rights/{access_right_id}", response_model=GroupAccessRight)
def remove_access_right_from_group(
    group_id: int,
    access_right_id: int,
    db: Session = Depends(get_db)
):
    db_group_access_right = group_access_right_service.delete_group_access_right(db, group_id, access_right_id)
    if db_group_access_right is None:
        raise HTTPException(status_code=404, detail="Group access right not found")
    return db_group_access_right

@router.post("/{group_id}/menus/", response_model=GroupMenu)
def add_menu_to_group(
    group_id: int,
    group_menu: GroupMenuCreate,
    db: Session = Depends(get_db)
):
    if group_menu.group_id != group_id:
        raise HTTPException(status_code=400, detail="Group ID in path and body do not match")
    db_group_menu = group_menu_service.get_group_menu(
        db, group_id, group_menu.menu_id
    )
    if db_group_menu:
        raise HTTPException(status_code=400, detail="Group menu already exists")
    return group_menu_service.create_group_menu(db=db, group_menu=group_menu)

@router.delete("/{group_id}/menus/{menu_id}", response_model=GroupMenu)
def remove_menu_from_group(
    group_id: int,
    menu_id: int,
    db: Session = Depends(get_db)
):
    db_group_menu = group_menu_service.delete_group_menu(db, group_id, menu_id)
    if db_group_menu is None:
        raise HTTPException(status_code=404, detail="Group menu not found")
    return db_group_menu
