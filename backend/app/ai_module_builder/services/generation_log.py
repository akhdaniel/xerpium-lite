from sqlalchemy.orm import Session
from backend.app.ai_module_builder.models.generation_log import GenerationLog
from backend.app.ai_module_builder.schemas.generation_log import GenerationLogCreate, GenerationLogUpdate
from typing import List, Optional

def create_generation_log(db: Session, log: GenerationLogCreate) -> GenerationLog:
    db_log = GenerationLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_generation_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(GenerationLog).offset(skip).limit(limit).all()

def get_generation_log(db: Session, log_id: int):
    return db.query(GenerationLog).filter(GenerationLog.id == log_id).first()

def update_generation_log(db: Session, log_id: int, log: GenerationLogUpdate) -> Optional[GenerationLog]:
    db_log = db.query(GenerationLog).filter(GenerationLog.id == log_id).first()
    if db_log:
        for key, value in log.dict(exclude_unset=True).items():
            setattr(db_log, key, value)
        db.commit()
        db.refresh(db_log)
    return db_log