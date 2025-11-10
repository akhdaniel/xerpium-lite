from sqlalchemy.orm import Session
from backend.app.base.menu_registry import register_menu_item

def register_ai_module_builder_menus(db: Session):
    register_menu_item(db, "ai_module_builder", {
        "id": 900,
        "name": "Dashboard",
        "path": "/ai_module_builder/dashboard",
        "icon": "dashboard-icon",
        "parent_id": None,
        "order": 0,
        "module": "ai_module_builder"
    })
    register_menu_item(db, "ai_module_builder", {
        "id": 902,
        "name": "Generation Logs",
        "path": "/ai_module_builder/generation_log",
        "icon": "list-icon",
        "parent_id": None,
        "order": 2,
        "module": "ai_module_builder"
    })
