from backend.app.base.menu_registry import register_menu_item
from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema
from sqlalchemy.orm import Session

class CustomerUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("customer")


    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Customers List",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "first_name", "headerName": "First Name", "type": "string"},
                        {"field": "last_name", "headerName": "Last Name", "type": "string"},
                        {"field": "email", "headerName": "Email", "type": "string"},
                        {"field": "phone_number", "headerName": "Phone Number", "type": "string"},
                        {"field": "birth_date", "headerName": "Birth Date", "type": "date"},
                        {"field": "last_contacted", "headerName": "Last Contacted", "type": "datetime"},
                    ]
                },
                "form": {
                    "title": "Customer Form",
                    "fields": [
                        {"field": "first_name", "label": "First Name", "type": "text", "required": True},
                        {"field": "last_name", "label": "Last Name", "type": "text", "required": True},
                        {"field": "email", "label": "Email", "type": "email", "required": True},
                        {"field": "phone_number", "label": "Phone Number", "type": "text", "required": False},
                        {"field": "birth_date", "label": "Birth Date", "type": "date", "required": False},
                        {"field": "last_contacted", "label": "Last Contacted", "type": "datetime", "required": False},
                        {"field": "addresses", "label": "Addresses", "type": "one2many", "related_model": "address", "module_name": "crm", 
                            "views": {
                                "list": {"title": "Addresses List", "columns": [{"field": "street", "headerName": "Street", "type": "string"}, {"field": "city", "headerName": "City", "type": "string"}, {"field": "state", "headerName": "State", "type": "string"}, {"field": "zip_code", "headerName": "Zip Code", "type": "string"}, {"field": "country", "headerName": "Country", "type": "many2one"}]}, 
                                "form": {"title": "Address Form", "fields": [{"field": "street", "label": "Street", "type": "text", "required": True}, {"field": "city", "label": "City", "type": "text", "required": True}, {"field": "state", "label": "State", "type": "text", "required": False}, {"field": "zip_code", "label": "Zip Code", "type": "text", "required": False}, {"field": "country", "label": "Country", "type": "autocomplete", "required": True, "url": "/base/country/autocomplete"}]}
                            }
                        }
                    ],
                    "layout": {
                        "type": "notebook",
                        "tabs": [
                            {
                                "label": "General",
                                "children": [
                                    {
                                        "type": "group",
                                        "direction": "row",
                                        "children": [
                                            {"field": "first_name"},
                                            {"field": "last_name"},
                                        ]
                                    },
                                    {
                                        "type": "group",
                                        "direction": "row",
                                        "children": [
                                           
                                            {"field": "email"},
                                            {"field": "phone_number"},                                ]
                                    },
                                    {
                                        "type": "group",
                                        "direction": "row",
                                        "children": [                                   
                                            {"field": "birth_date"},
                                            {"field": "last_contacted"},   
                                        ]
                                    }
                                ]
                            },
                            {
                                "label": "Addresses",
                                "children": [
                                    {"field": "addresses"}
                                ]
                            }
                        ]
                    }
                }
            }
        }



register_ui_schema(CustomerUISchema())
