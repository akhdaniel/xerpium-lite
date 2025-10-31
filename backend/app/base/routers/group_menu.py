from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.base.schemas.group_menu import GroupMenu, GroupMenuCreate
from backend.app.base.services import group_menu as group_menu_service
from backend.app.database import get_db

router = APIRouter()

@router.post("/", response_model=GroupMenu)
def create_group_menu(group_menu: GroupMenuCreate, db: Session = Depends(get_db)):
    db_group_menu = group_menu_service.get_group_menu(
        db, group_menu.group_id, group_menu.menu_id
    )
    if db_group_menu:
        raise HTTPException(status_code=400, detail="Group menu already exists")
    return group_menu_service.create_group_menu(db=db, group_menu=group_menu)

@router.get("/group/{group_id}", response_model=List[GroupMenu])
def read_group_menus_by_group(group_id: int, db: Session = Depends(get_db)):
    group_menus = group_menu_service.get_group_menus_by_group(db, group_id)
    return group_menus

@router.delete("/{group_id}/{menu_id}", response_model=GroupMenu)
def delete_group_menu(group_id: int, menu_id: int, db: Session = Depends(get_db)):
    db_group_menu = group_menu_service.delete_group_menu(db, group_id, menu_id)
    if db_group_menu is None:
        raise HTTPException(status_code=404, detail="Group menu not found")
    return db_group_menu
