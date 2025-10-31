from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class AccessRightUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("accessrights")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Access Right List",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "name", "headerName": "Name", "type": "string"},
                        {"field": "description", "headerName": "Description", "type": "string"},
                        {"field": "created_at", "headerName": "Created At", "type": "datetime"},
                        {"field": "updated_at", "headerName": "Updated At", "type": "datetime"}
                    ]
                },
                "form": {
                    "title": "Access Right Form",
                    "fields": [
                        {"field": "name", "label": "Name", "type": "text", "required": True},
                        {"field": "description", "label": "Description", "type": "textarea", "required": False},
                    ]
                }
            }
        }

register_ui_schema(AccessRightUISchema())
