from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class GroupAccessRightUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("GroupAccessRight")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Group Access Right List",
                    "columns": [
                        {"field": "group_id", "headerName": "Group ID", "type": "number"},
                        {"field": "access_right_id", "headerName": "Access Right ID", "type": "number"},
                        {"field": "can_read", "headerName": "Can Read", "type": "boolean"},
                        {"field": "can_create", "headerName": "Can Create", "type": "boolean"},
                        {"field": "can_update", "headerName": "Can Update", "type": "boolean"},
                        {"field": "can_delete", "headerName": "Can Delete", "type": "boolean"},
                        {"field": "created_at", "headerName": "Created At", "type": "datetime"},
                        {"field": "updated_at", "headerName": "Updated At", "type": "datetime"}
                    ]
                },
                "form": {
                    "title": "Group Access Right Form",
                    "fields": [
                        {"field": "group_id", "label": "Group", "type": "select", "options_url": "/groups", "required": True},
                        {"field": "access_right_id", "label": "Access Right", "type": "select", "options_url": "/access_rights", "required": True},
                        {"field": "can_read", "label": "Can Read", "type": "checkbox", "required": False, "default": False},
                        {"field": "can_create", "label": "Can Create", "type": "checkbox", "required": False, "default": False},
                        {"field": "can_update", "label": "Can Update", "type": "checkbox", "required": False, "default": False},
                        {"field": "can_delete", "label": "Can Delete", "type": "checkbox", "required": False, "default": False},
                    ]
                }
            }
        }

register_ui_schema(GroupAccessRightUISchema())

