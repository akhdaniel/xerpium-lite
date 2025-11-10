from sqlalchemy.orm import Session
from backend.app.base.dashboard_registry import register_dashboard_item

def get_dummy_data(db: Session):
    return "AI Ready"

def get_dummy_data2(db: Session):
    return "10"

def register_ai_module_builder_dashboard_items():
    register_dashboard_item("ai_module_builder", {
        "id": "ai_module_builder_status",
        "title": "AI Module Builder Status",
        "type": "kpi_card",
        "service": get_dummy_data,
    })

    register_dashboard_item("ai_module_builder", {
        "id": "ai_module_builder_apps",
        "title": "Number of Apps",
        "type": "kpi_card",
        "service": get_dummy_data2,
    })
