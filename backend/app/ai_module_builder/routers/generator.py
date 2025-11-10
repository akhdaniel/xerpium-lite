from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.ai_module_builder.schemas.model_info import ModelInfo # Import the Pydantic ModelInfo

from backend.app.database import get_db
from backend.app.ai_module_builder.schemas.generation_log import GenerationLog
from backend.app.ai_module_builder.services import generation_log as generation_log_service

router = APIRouter()

