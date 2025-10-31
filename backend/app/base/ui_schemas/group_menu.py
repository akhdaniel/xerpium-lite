from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class GroupMenuUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("GroupMenu")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Group Menu List",
                    "columns": [
                        {"field": "group_id", "headerName": "Group ID", "type": "number"},
                        {"field": "menu_id", "headerName": "Menu ID", "type": "number"},
                        {"field": "created_at", "headerName": "Created At", "type": "datetime"},
                        {"field": "updated_at", "headerName": "Updated At", "type": "datetime"}
                    ]
                },
                "form": {
                    "title": "Group Menu Form",
                    "fields": [
                        {"field": "group_id", "label": "Group", "type": "select", "options_url": "/groups", "required": True},
                        {"field": "menu_id", "label": "Menu", "type": "select", "options_url": "/menus", "required": True},
                    ]
                }
            }
        }

register_ui_schema(GroupMenuUISchema())
