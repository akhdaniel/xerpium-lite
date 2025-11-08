from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.base.schemas.module import Module, ModuleCreate, ModuleUpdate
from backend.app.base.services import module as module_service

router = APIRouter()

@router.post("/", response_model=Module)
def create_module(module: ModuleCreate, db: Session = Depends(get_db)):
    db_module = module_service.get_module_by_name(db, name=module.name)
    if db_module:
        raise HTTPException(status_code=400, detail="Module name already registered")
    return module_service.create_module(db=db, module=module)

@router.get("/", response_model=List[Module])
def read_modules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    modules = module_service.get_modules(db, skip=skip, limit=limit)
    return modules

@router.get("/{module_id}", response_model=Module)
def read_module(module_id: int, db: Session = Depends(get_db)):
    db_module = module_service.get_module(db, module_id=module_id)
    if db_module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return db_module

@router.put("/{module_id}", response_model=Module)
def update_module(module_id: int, module: ModuleUpdate, db: Session = Depends(get_db)):
    db_module = module_service.update_module(db, module_id=module_id, module=module)
    if db_module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return db_module

@router.delete("/{module_id}", response_model=Module)
def delete_module(module_id: int, db: Session = Depends(get_db)):
    db_module = module_service.delete_module(db, module_id=module_id)
    if db_module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return db_module
