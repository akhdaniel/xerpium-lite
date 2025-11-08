from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class LocationUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("locations")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Locations List",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "name", "headerName": "Name", "type": "string"},
                        {"field": "warehouse.name", "headerName": "Warehouse", "type": "string"},
                    ]
                },
                "form": {
                    "title": "Location Form",
                    "fields": [
                        {"field": "name", "label": "Name", "type": "text", "required": True},
                        {"field": "warehouse_id", "label": "Warehouse", "type": "select", "options_url": "/inventory/warehouses", "required": True},
                    ]
                }
            }
        }

register_ui_schema(LocationUISchema())
