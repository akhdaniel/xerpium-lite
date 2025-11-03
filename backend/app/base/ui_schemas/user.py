from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class UserUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("users")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "User List",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "username", "headerName": "Username", "type": "string"},
                        {"field": "email", "headerName": "Email", "type": "string"},
                        {"field": "created_at", "headerName": "Created At", "type": "datetime"},
                        {"field": "updated_at", "headerName": "Updated At", "type": "datetime"}
                    ]
                },
                "form": {
                    "title": "User Form",
                    "fields": [
                        {"field": "username", "label": "Username", "type": "text", "required": True},
                        {"field": "email", "label": "Email", "type": "email", "required": True},
                        {"field": "password", "label": "Password", "type": "password", "required": True},
                    ],
                    "layout": {
                        "type": "group",
                        "direction": "row",
                        "children": [
                            {
                                "type": "group",
                                "direction": "column",
                                "children": [
                                    {"field": "username"},
                                    {"field": "email"}
                                ]
                            },
                            {
                                "type": "group",
                                "direction": "column",
                                "children": [
                                    {"field": "password"}
                                ]
                            }
                        ]
                    }
                }
            }
        }

register_ui_schema(UserUISchema())
