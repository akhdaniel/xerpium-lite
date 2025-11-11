from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class GeneratorUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("generation_log")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Module Generator",
                    "columns": [
                        {"field": "module_name", "headerName": "Module Name"},
                        {"field": "created_at", "headerName": "Generated At"},
                    ]
                },
                "form": {
                    "title": "Generate New Module",
                    "fields": [
                        {
                            "field": "module_name",
                            "label": "New Module Name",
                            "type": "text",
                            "required": True,
                            "props": {"placeholder": "e.g., blog"}
                        },
                        {
                            "field": "specification",
                            "label": "Specification",
                            "type": "textarea",
                            "required": True,
                            "props": {
                                "rows": 10,
                                "placeholder": "e.g., Create a model named 'Post' with fields: title (string), content (text), is_published (boolean)."
                            }
                        },
                        {
                            "field": "detailed_specification",
                            "label": "Detailed Specification",
                            "type": "textarea",
                            "required": False,
                            "props": {
                                "rows": 15,
                                "placeholder": "Provide a more detailed specification for the module, including relationships, specific field constraints, etc."
                            }
                        }
                    ],
                    "actions": [
                        {
                            "label": "Generate Module",
                            "route": "/ai_module_builder/generation_log/generate",
                            "action_type": "api_call",
                            "method": "POST"
                        }
                    ]
                }
            }
        }

register_ui_schema(GeneratorUISchema())
