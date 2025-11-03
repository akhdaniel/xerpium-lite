from backend.app.base.menu_registry import register_menu_item
from sqlalchemy.orm import Session

def register_crm_menus(db: Session):
    register_menu_item(db, "crm", {
        "id": 5,
        "name": "Customers",
        "path": "/customer",
        "icon": "customers-icon",
        "parent_id": None,
        "order": 1,
        "module": "crm"
    })
    register_menu_item(db, "crm", {
        "id": 6,
        "name": "Leads",
        "path": "/leads",
        "icon": "leads-icon",
        "parent_id": None,
        "order": 2,
        "module": "crm"
    })
    register_menu_item(db, "crm", {
        "id": 7,
        "name": "Opportunities",
        "path": "/opportunities",
        "icon": "opportunities-icon",
        "parent_id": None,
        "order": 3,
        "module": "crm"
    })
