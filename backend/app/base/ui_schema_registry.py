from typing import Dict, Any

ui_schemas: Dict[str, Any] = {}

def register_ui_schema(schema_instance):
    ui_schemas[schema_instance.model_name] = schema_instance

def get_ui_schema(model_name: str):
    return ui_schemas.get(model_name)
