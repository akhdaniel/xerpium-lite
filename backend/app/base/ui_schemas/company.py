from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class CompanyUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("company")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Companies",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "name", "headerName": "Name", "type": "string"},
                    ]
                },
                "form": {
                    "title": "Company Form",
                    "fields": [
                        {"field": "name", "label": "Name", "type": "text", "required": True},
                    ]
                }
            }
        }

register_ui_schema(CompanyUISchema())
