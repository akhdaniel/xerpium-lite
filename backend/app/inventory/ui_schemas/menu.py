from sqlalchemy.orm import Session
from backend.app.base.menu_registry import register_menu_item

def register_inventory_menus(db: Session):
    register_menu_item(db, "inventory", {
        "id": 200, # Use a unique ID for your module's menus
        "name": "Inventory Dashboard",
        "path": "/inventory/dashboard",
        "icon": "inventory-dashboard-icon",
        "parent_id": None,
        "order": 0,
        "module": "inventory"
    })
    register_menu_item(db, "inventory", {
        "id": 201,
        "name": "Products",
        "path": "/inventory/products",
        "icon": "products-icon",
        "parent_id": None,
        "order": 1,
        "module": "inventory"
    })
    register_menu_item(db, "inventory", {
        "id": 202,
        "name": "Warehouses",
        "path": "/inventory/warehouses",
        "icon": "warehouses-icon",
        "parent_id": None,
        "order": 2,
        "module": "inventory"
    })
    register_menu_item(db, "inventory", {
        "id": 203,
        "name": "Locations",
        "path": "/inventory/locations",
        "icon": "locations-icon",
        "parent_id": None,
        "order": 3,
        "module": "inventory"
    })
    register_menu_item(db, "inventory", {
        "id": 204,
        "name": "Inventory Movements",
        "path": "/inventory/movements",
        "icon": "inventory-movements-icon",
        "parent_id": None,
        "order": 4,
        "module": "inventory"
    })
