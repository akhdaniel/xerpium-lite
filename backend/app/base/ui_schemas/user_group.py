from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class UserGroupUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("UserGroup")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "User Group List",
                    "columns": [
                        {"field": "user_id", "headerName": "User ID", "type": "number"},
                        {"field": "group_id", "headerName": "Group ID", "type": "number"},
                        {"field": "created_at", "headerName": "Created At", "type": "datetime"},
                        {"field": "updated_at", "headerName": "Updated At", "type": "datetime"}
                    ]
                },
                "form": {
                    "title": "User Group Form",
                    "fields": [
                        {"field": "user_id", "label": "User", "type": "select", "options_url": "/users", "required": True},
                        {"field": "group_id", "label": "Group", "type": "select", "options_url": "/groups", "required": True},
                    ]
                }
            }
        }

register_ui_schema(UserGroupUISchema())
