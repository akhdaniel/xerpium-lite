from sqlalchemy.orm import Session
from backend.app.base.models.module import Module
from backend.app.base.schemas.module import ModuleCreate, ModuleUpdate

def get_module(db: Session, module_id: int):
    return db.query(Module).filter(Module.id == module_id).first()

def get_module_by_name(db: Session, name: str):
    return db.query(Module).filter(Module.name == name).first()

def get_modules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Module).offset(skip).limit(limit).all()

def create_module(db: Session, module: ModuleCreate):
    db_module = Module(**module.dict())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

def update_module(db: Session, module_id: int, module: ModuleUpdate):
    db_module = get_module(db, module_id)
    if db_module:
        update_data = module.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_module, key, value)
        db.commit()
        db.refresh(db_module)
    return db_module

def delete_module(db: Session, module_id: int):
    db_module = get_module(db, module_id)
    if db_module:
        db.delete(db_module)
        db.commit()
    return db_module