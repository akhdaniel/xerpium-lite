from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class LeadUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("leads")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Leads List",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "first_name", "headerName": "First Name", "type": "string"},
                        {"field": "last_name", "headerName": "Last Name", "type": "string"},
                        {"field": "email", "headerName": "Email", "type": "string"},
                        {"field": "phone_number", "headerName": "Phone Number", "type": "string"},
                        {"field": "company", "headerName": "Company", "type": "string"},
                        {"field": "status", "headerName": "Status", "type": "string"},
                        {"field": "created_at", "headerName": "Created At", "type": "datetime"},
                        {"field": "updated_at", "headerName": "Updated At", "type": "datetime"}
                    ]
                },
                "form": {
                    "title": "Lead Form",
                    "fields": [
                        {"field": "first_name", "label": "First Name", "type": "text", "required": True},
                        {"field": "last_name", "label": "Last Name", "type": "text", "required": True},
                        {"field": "email", "label": "Email", "type": "email", "required": True},
                        {"field": "phone_number", "label": "Phone Number", "type": "text", "required": False},
                        {"field": "company", "label": "Company", "type": "text", "required": False},
                        {"field": "status", "label": "Status", "type": "text", "required": False},
                    ]
                }
            }
        }

register_ui_schema(LeadUISchema())
