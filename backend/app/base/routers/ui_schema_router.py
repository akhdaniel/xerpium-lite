from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from backend.app.base.ui_schema_registry import get_ui_schema
from backend.app.base.dependencies import has_permission

router = APIRouter()

@router.get("/{model_name}", response_model=Dict[str, Any], dependencies=[Depends(has_permission("UI_Schema", "read"))])
def get_model_ui_schema(model_name: str):
    schema = get_ui_schema(model_name)
    if not schema:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"UI Schema for model {model_name} not found")
    return schema.get_ui_schema()
