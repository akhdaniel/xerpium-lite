from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema
import json

class UISchemasUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("ui_schemas")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "UI Schemas List",
                    "columns": [
                        {"field": "model_name", "headerName": "Model Name", "type": "string"},
                    ]
                },
                "form": {
                    "title": "UI Schema Details",
                    "fields": [
                        {"field": "schema_json", "label": "Schema JSON", "type": "textarea", "props": {"rows": 40, "readonly": True}},
                    ]
                }
            }
        }

register_ui_schema(UISchemasUISchema())