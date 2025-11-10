from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.ai_module_builder.schemas.model_info import ModelInfo # Import the Pydantic ModelInfo

from backend.app.database import get_db
from backend.app.ai_module_builder.schemas.generation_log import GenerationLog
from backend.app.ai_module_builder.services import generation_log as generation_log_service
from backend.app.ai_module_builder.services import generation_service

router = APIRouter()

@router.post("/generate/{generation_log_id}", response_model=dict)
def generate_module_from_log(generation_log_id: int, db: Session = Depends(get_db)):
    try:
        result = generation_service.generate_module_by_log_id(db, generation_log_id)
        return {"message": "Module generation initiated successfully", "details": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Module generation failed: {str(e)}")