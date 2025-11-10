from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.app.base.dashboard_registry import get_dashboard_items_by_module
from backend.app.database import get_db
from backend.app.base.dependencies import has_permission

router = APIRouter()

@router.get("/dashboard", response_model=List[Dict[str, Any]], dependencies=[Depends(has_permission("Dashboard", "read"))])
def get_dashboard_items(db: Session = Depends(get_db)):
    items = get_dashboard_items_by_module("ai_module_builder")
    results = []
    for item in items:
        # Execute the service function to get the value
        value = item["service"](db)
        results.append({
            "id": item["id"],
            "title": item["title"],
            "value": value,
            "type": item["type"],
            "chart_type": item.get("chart_type"),
            "module": "ai_module_builder"
        })
    return results
