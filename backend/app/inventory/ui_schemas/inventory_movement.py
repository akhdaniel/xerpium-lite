from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class InventoryMovementUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("movements")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Inventory Movements List",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "product.name", "headerName": "Product", "type": "string"},
                        {"field": "source_location.name", "headerName": "Source Location", "type": "string"},
                        {"field": "destination_location.name", "headerName": "Destination Location", "type": "string"},
                        {"field": "quantity", "headerName": "Quantity", "type": "number"},
                        {"field": "movement_date", "headerName": "Movement Date", "type": "datetime"},
                    ]
                },
                "form": {
                    "title": "Inventory Movement Form",
                    "fields": [
                        {"field": "product_id", "label": "Product", "type": "select", "options_url": "/inventory/products", "required": True},
                        {"field": "source_location_id", "label": "Source Location", "type": "select", "options_url": "/inventory/locations", "required": False},
                        {"field": "destination_location_id", "label": "Destination Location", "type": "select", "options_url": "/inventory/locations", "required": True},
                        {"field": "quantity", "label": "Quantity", "type": "number", "required": True},
                        {"field": "movement_date", "label": "Movement Date", "type": "datetime", "required": True},
                    ]
                }
            }
        }

register_ui_schema(InventoryMovementUISchema())
