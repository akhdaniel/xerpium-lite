from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class OpportunityUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("opportunities")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Opportunities List",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "name", "headerName": "Name", "type": "string"},
                        {"field": "description", "headerName": "Description", "type": "string"},
                        {"field": "amount", "headerName": "Amount", "type": "number"},
                        {"field": "stage", "headerName": "Stage", "type": "string"},
                        {"field": "close_date", "headerName": "Close Date", "type": "date"},
                        {"field": "lead_id", "headerName": "Lead ID", "type": "number"},
                        {"field": "created_at", "headerName": "Created At", "type": "datetime"},
                        {"field": "updated_at", "headerName": "Updated At", "type": "datetime"}
                    ]
                },
                "form": {
                    "title": "Opportunity Form",
                    "fields": [
                        {"field": "name", "label": "Name", "type": "text", "required": True},
                        {"field": "description", "label": "Description", "type": "textarea", "required": False},
                        {"field": "amount", "label": "Amount", "type": "number", "required": True},
                        {"field": "stage", "label": "Stage", "type": "text", "required": False},
                        {"field": "close_date", "label": "Close Date", "type": "date", "required": False},
                        {"field": "lead_id", "label": "Lead", "type": "select", "options_url": "/crm/leads", "required": False},
                    ]
                }
            }
        }

register_ui_schema(OpportunityUISchema())
