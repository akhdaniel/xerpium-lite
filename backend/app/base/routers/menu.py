from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.base.schemas.menu import Menu, MenuCreate, MenuUpdate
from backend.app.base.services import menu as menu_service
from backend.app.database import get_db

router = APIRouter()

@router.post("/", response_model=Menu)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    return menu_service.create_menu(db=db, menu=menu)

@router.get("/", response_model=List[Menu])
def read_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    menus = menu_service.get_menus(db, skip=skip, limit=limit)
    return menus

@router.get("/{menu_id}", response_model=Menu)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = menu_service.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu

@router.put("/{menu_id}", response_model=Menu)
def update_menu(menu_id: int, menu: MenuUpdate, db: Session = Depends(get_db)):
    db_menu = menu_service.update_menu(db, menu_id=menu_id, menu=menu)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu

@router.delete("/{menu_id}", response_model=Menu)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = menu_service.delete_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu
