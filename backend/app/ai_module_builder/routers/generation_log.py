from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.ai_module_builder.schemas.module_generation import ModuleSpecification
from backend.app.ai_module_builder.schemas.model_info import ModelInfo # Import the Pydantic ModelInfo
from backend.app.ai_module_builder.schemas.generation_log import GenerationLog, GenerationLogCreate, GenerationLogUpdate

from backend.app.database import get_db
from backend.app.ai_module_builder.schemas.generation_log import GenerationLog
from backend.app.ai_module_builder.services import generation_log as generation_log_service

router = APIRouter()

@router.get("/", response_model=List[GenerationLog])
def read_generation_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = generation_log_service.get_generation_logs(db, skip=skip, limit=limit)
    return logs

@router.get("/{log_id}", response_model=GenerationLog)
def read_generation_log(log_id: int, db: Session = Depends(get_db)):
    db_log = generation_log_service.get_generation_log(db, log_id=log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Generation log not found")
    return db_log

@router.post("/", response_model=GenerationLog)
def create_generation_log(generation_log: GenerationLogCreate, db: Session = Depends(get_db)):
    return generation_log_service.create_generation_log(db=db, log=generation_log)

@router.put("/{log_id}", response_model=GenerationLog)
def update_lead(log_id: int, log: GenerationLogUpdate, db: Session = Depends(get_db)):
    db_log = generation_log_service.update_generation_log(db, log_id=log_id, log=log)
    if db_log is None:
        raise HTTPException(status_code=404, detail="GenerationLog not found")
    return db_log

@router.post("/generate", response_model=ModelInfo) # Use the Pydantic ModelInfo
def generate_module_endpoint(
    spec: ModuleSpecification,
    db: Session = Depends(get_db)
):
    """
    Endpoint to generate a new module from a specification.
    This is triggered by the 'Save' action in the GenericModelView.
    """
    result = generation_log_service.generate_module_files(db, spec)
    # The GenericModelView expects the created object back.
    # We don't really have one. We'll return the first model info as a proxy.
    models = generation_log_service._parse_specification(spec.specification)
    if models:
        return models[0]
    return {}