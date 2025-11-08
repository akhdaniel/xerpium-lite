from backend.app.base.menu_registry import register_menu_item
from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema
from sqlalchemy.orm import Session

class MenuUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("menus")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Menu List",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "name", "headerName": "Name", "type": "string"},
                        {"field": "path", "headerName": "Path", "type": "string"},
                        {"field": "icon", "headerName": "Icon", "type": "string"},
                        {"field": "parent_id", "headerName": "Parent ID", "type": "number"},
                        {"field": "order", "headerName": "Order", "type": "number"},
                        {"field": "created_at", "headerName": "Created At", "type": "datetime"},
                        {"field": "updated_at", "headerName": "Updated At", "type": "datetime"}
                    ]
                },
                "form": {
                    "title": "Menu Form",
                    "fields": [
                        {"field": "name", "label": "Name", "type": "text", "required": True},
                        {"field": "path", "label": "Path", "type": "text", "required": True},
                        {"field": "icon", "label": "Icon", "type": "text", "required": False},
                        {"field": "parent_id", "label": "Parent Menu", "type": "autocomplete", "url": "/base/menus", "required": False},
                        {"field": "order", "label": "Order", "type": "number", "required": False, "default": 0},
                    ]
                }
            }
        }

def register_base_menus(db: Session):
    register_menu_item(db, "base", {
        "id": 9,
        "name": "Dashboard",
        "path": "/base/dashboard",
        "icon": "dashboard-icon",
        "parent_id": None,
        "order": 0,
        "module": "base"
    })
    register_menu_item(db, "base", {
        "id": 10,
        "name": "Settings",
        "path": None,
        "icon": "settings-icon",
        "parent_id": None,
        "order": 1,
        "module": "base"
    })
    register_menu_item(db, "base", {
        "id": 1,
        "name": "Users",
        "path": "/users",
        "icon": "users-icon",
        "parent_id": 10,
        "order": 1,
        "module": "base"
    })
    register_menu_item(db, "base", {
        "id": 2,
        "name": "Groups",
        "path": "/groups",
        "icon": "groups-icon",
        "parent_id": 10,
        "order": 2,
        "module": "base"
    })
    register_menu_item(db, "base", {
        "id": 3,
        "name": "Access Rights",
        "path": "/access_rights",
        "icon": "access-rights-icon",
        "parent_id": 10,
        "order": 3,
        "module": "base"
    })
    register_menu_item(db, "base", {
        "id": 4,
        "name": "Menus",
        "path": "/menus",
        "icon": "menus-icon",
        "parent_id": 10,
        "order": 4,
        "module": "base"
    })
    register_menu_item(db, "base", {
        "id": 101,
        "name": "Companies",
        "path": "/company",
        "icon": "companies-icon",
        "parent_id": 10,
        "order": 5,
        "module": "base"
    })
    register_menu_item(db, "base", {
        "id": 100,
        "name": "Countries",
        "path": "/country",
        "icon": "countries-icon",
        "parent_id": None,
        "order": 5,
        "module": "base"
    })
    register_menu_item(db, "base", {
        "id": 102,
        "name": "UI Schemas",
        "path": "/ui_schemas",
        "icon": "ui-schemas-icon",
        "parent_id": 10,
        "order": 6,
        "module": "base"
    })
    register_menu_item(db, "base", {
        "id": 103,
        "name": "Modules",
        "path": "/modules",
        "icon": "modules-icon",
        "parent_id": 10,
        "order": 7,
        "module": "base"
    })

register_ui_schema(MenuUISchema())

