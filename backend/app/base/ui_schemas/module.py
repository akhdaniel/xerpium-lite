from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class ModuleUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("modules")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Modules List",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "name", "headerName": "Name", "type": "string"},
                        {"field": "is_active", "headerName": "Is Active", "type": "boolean"},
                    ]
                },
                "form": {
                    "title": "Module Form",
                    "fields": [
                        {"field": "name", "label": "Name", "type": "text", "required": True},
                        {"field": "is_active", "label": "Is Active", "type": "checkbox", "required": True},
                    ]
                }
            }
        }

register_ui_schema(ModuleUISchema())
