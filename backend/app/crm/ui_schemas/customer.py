from backend.app.base.menu_registry import register_menu_item
from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema
from sqlalchemy.orm import Session

class CustomerUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("customers")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Customers List",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "first_name", "headerName": "First Name", "type": "string"},
                        {"field": "last_name", "headerName": "Last Name", "type": "string"},
                        {"field": "email", "headerName": "Email", "type": "string"},
                        {"field": "phone_number", "headerName": "Phone Number", "type": "string"},
                        {"field": "address", "headerName": "Address", "type": "string"},
                        {"field": "birth_date", "headerName": "Birth Date", "type": "date"},
                        {"field": "last_contacted", "headerName": "Last Contacted", "type": "datetime"},
                        # {"field": "created_at", "headerName": "Created At", "type": "datetime"},
                        # {"field": "updated_at", "headerName": "Updated At", "type": "datetime"},
                        {"field": "country.name", "headerName": "Country", "type": "string"}
                    ]
                },
                "form": {
                    "title": "Customer Form",
                    "fields": [
                        {"field": "first_name", "label": "First Name", "type": "text", "required": True},
                        {"field": "last_name", "label": "Last Name", "type": "text", "required": True},
                        {"field": "email", "label": "Email", "type": "email", "required": True},
                        {"field": "phone_number", "label": "Phone Number", "type": "text", "required": False},
                        {"field": "address", "label": "Address", "type": "textarea", "required": False},
                        {"field": "country_id", "label": "Country", "type": "many2one", "related_model": "country", "module_name": "crm", "required": False},
                        {"field": "birth_date", "label": "Birth Date", "type": "date", "required": False},
                        {"field": "last_contacted", "label": "Last Contacted", "type": "datetime", "required": False}
                    ]
                }
            }
        }

def register_crm_menus(db: Session):
    register_menu_item(db, "crm", {
        "id": 5,
        "name": "Customers",
        "path": "/customers",
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
    register_menu_item(db, "crm", {
        "id": 8,
        "name": "Countries",
        "path": "/countries",
        "icon": "countries-icon",
        "parent_id": None,
        "order": 4,
        "module": "crm"
    })

register_ui_schema(CustomerUISchema())
