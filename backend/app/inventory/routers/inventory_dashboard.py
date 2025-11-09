from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.app.database import get_db
from backend.app.inventory.services import product as product_service
from backend.app.inventory.services import warehouse as warehouse_service
from backend.app.inventory.services import location as location_service
from backend.app.base.dashboard_registry import get_dashboard_items_by_module

router = APIRouter()

@router.get("/dashboard")
def get_inventory_dashboard_page(db: Session = Depends(get_db)):
    items = get_dashboard_items_by_module("inventory")
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
            "module": "crm"
        })
    return results

@router.get("/dashboard_items", response_model=List[Dict[str, Any]])
def read_dashboard_items():
    return get_dashboard_items_by_module('inventory')

@router.get("/dashboard/products_count")
def get_products_count(db: Session = Depends(get_db)):
    return {"value": len(product_service.get_products(db))}

@router.get("/dashboard/warehouses_count")
def get_warehouses_count(db: Session = Depends(get_db)):
    return {"value": len(warehouse_service.get_warehouses(db))}

@router.get("/dashboard/locations_count")
def get_locations_count(db: Session = Depends(get_db)):
    return {"value": len(location_service.get_locations(db))}
