from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.app.base.menu_registry import get_all_menu_items, build_menu_hierarchy, get_menu_items_by_module
from backend.app.base.dependencies import has_permission
from backend.app.database import get_db

router = APIRouter()

@router.get("/hierarchy", response_model=List[Dict[str, Any]], dependencies=[Depends(has_permission("Menu", "read"))])
def get_menu_hierarchy(db: Session = Depends(get_db)):
    all_items = get_all_menu_items(db)
    hierarchy = build_menu_hierarchy(all_items)
    return hierarchy

@router.get("/{module_name}", response_model=List[Dict[str, Any]], dependencies=[Depends(has_permission("Menu", "read"))])
def get_module_menu_hierarchy(module_name: str, db: Session = Depends(get_db)):
    module_items = get_menu_items_by_module(db, module_name)
    hierarchy = build_menu_hierarchy(module_items)
    return hierarchy
