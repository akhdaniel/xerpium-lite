import os
import re
from typing import List
from sqlalchemy.orm import Session
from backend.app.ai_module_builder.schemas.module_generation import ModuleSpecification
from backend.app.ai_module_builder.schemas.generation_log import GenerationLogCreate
from backend.app.ai_module_builder.schemas.model_info import FieldInfo, ModelInfo # Import Pydantic versions
from backend.app.ai_module_builder.services import generation_log as generation_log_service
from openai import OpenAI # Import OpenAI client
from dotenv import load_dotenv
load_dotenv()

import json
from pathlib import Path

# --- Data Structures for Parsed Spec ---
# Removed internal FieldInfo and ModelInfo classes, now using Pydantic versions

# --- Type Mapping ---

def _map_type_to_sqlalchemy(field_type: str):
    type_map = {
        "string": "String",
        "text": "String",
        "integer": "Integer",
        "float": "Float",
        "boolean": "Boolean",
        "datetime": "DateTime",
        "date": "Date",
    }
    return type_map.get(field_type.lower(), "String")

def _map_type_to_pydantic(field_type: str):
    type_map = {
        "string": "str",
        "text": "str",
        "integer": "int",
        "float": "float",
        "boolean": "bool",
        "datetime": "datetime",
        "date": "date",
    }
    return type_map.get(field_type.lower(), "str")

def _get_pydantic_imports(models):
    imports = set()
    for model in models:
        for field in model.fields:
            if field.field_type.lower() in ["datetime", "date"]:
                imports.add("from datetime import datetime, date")
    return "\n".join(imports)

# --- Code Generation Templates ---

def _generate_model_code(module_name: str, model: ModelInfo) -> str:
    model_name_pascal = model.name.capitalize()
    table_name = model.name.lower() + "s"
    
    columns = []
    for field in model.fields:
        sqlalchemy_type = _map_type_to_sqlalchemy(field.field_type)
        nullable = "False" if field.name == 'name' else "True"
        columns.append(f"    {field.name} = Column({sqlalchemy_type}, nullable={nullable})")

    return f"""from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Date\nfrom backend.app.database import Base\n\nclass {model_name_pascal}(Base):\n    __tablename__ = \"{table_name}\"\n\n    id = Column(Integer, primary_key=True, index=True)\n{chr(10).join(columns)}\n"""

def _generate_schema_code(module_name: str, model: ModelInfo) -> str:
    model_name_pascal = model.name.capitalize()
    pydantic_imports = _get_pydantic_imports([model])

    base_fields = []
    for field in model.fields:
        pydantic_type = _map_type_to_pydantic(field.field_type)
        base_fields.append(f"    {field.name}: {pydantic_type}")

    return f"""from pydantic import BaseModel\nfrom typing import Optional\n{pydantic_imports}\n\nclass {model_name_pascal}Base(BaseModel):\n{chr(10).join(base_fields)}\n\nclass {model_name_pascal}Create({model_name_pascal}Base):\n    pass\n\nclass {model_name_pascal}Update(BaseModel):\n{chr(10).join([f'    {f.name}: Optional[{_map_type_to_pydantic(f.field_type)}] = None' for f in model.fields])}\n\nclass {model_name_pascal}({model_name_pascal}Base):\n    id: int\n\n    class Config:\n        orm_mode = True\n"""

def _generate_service_code(module_name: str, model: ModelInfo) -> str:
    model_name_pascal = model.name.capitalize()
    model_name_lower = model.name.lower()
    
    return f"""from sqlalchemy.orm import Session\nfrom backend.app.{module_name}.models.{model_name_lower} import {model_name_pascal}\nfrom backend.app.{module_name}.schemas.{model_name_lower} import {model_name_pascal}Create, {model_name_pascal}Update\n\ndef get_{model_name_lower}(db: Session, {model_name_lower}_id: int):\n    return db.query({model_name_pascal}).filter({model_name_pascal}.id == {model_name_lower}_id).first()\n\ndef get_{model_name_lower}s(db: Session, skip: int = 0, limit: int = 100):\n    return db.query({model_name_pascal}).offset(skip).limit(limit).all()\n\ndef create_{model_name_lower}(db: Session, {model_name_lower}: {model_name_pascal}Create):\n    db_{model_name_lower} = {model_name_pascal}(**{model_name_lower}.dict())\n    db.add(db_{model_name_lower})\n    db.commit()\n    db.refresh(db_{model_name_lower})\n    return db_{model_name_lower}\n\ndef update_{model_name_lower}(db: Session, {model_name_lower}_id: int, {model_name_lower}: {model_name_pascal}Update):\n    db_{model_name_lower} = get_{model_name_lower}(db, {model_name_lower}_id)\n    if db_{model_name_lower}:\n        update_data = {model_name_lower}.dict(exclude_unset=True)\n        for key, value in update_data.items():\n            setattr(db_{model_name_lower}, key, value)\n        db.commit()\n        db.refresh(db_{model_name_lower})\n    return db_{model_name_lower}\n\ndef delete_{model_name_lower}(db: Session, {model_name_lower}_id: int):\n    db_{model_name_lower} = get_{model_name_lower}(db, {model_name_lower}_id)\n    if db_{model_name_lower}:\n        db.delete(db_{model_name_lower})\n        db.commit()\n    return db_{model_name_lower}\n"""

def _generate_router_code(module_name: str, model: ModelInfo) -> str:
    model_name_pascal = model.name.capitalize()
    model_name_lower = model.name.lower()
    path_param_name = f"{model_name_lower}_id"
    path_single = f"/{{\"{path_param_name}\"}}"

    return f"""from fastapi import APIRouter, Depends, HTTPException\nfrom sqlalchemy.orm import Session\nfrom typing import List\n\nfrom backend.app.database import get_db\nfrom backend.app.{module_name}.schemas.{model_name_lower} import {model_name_pascal}, {model_name_pascal}Create, {model_name_pascal}Update\nfrom backend.app.{module_name}.services import {model_name_lower} as {model_name_lower}_service\n\nrouter = APIRouter()\n\n@router.post("/", response_model={model_name_pascal})\ndef create_{model_name_lower}_endpoint({model_name_lower}: {model_name_pascal}Create, db: Session = Depends(get_db)):\n    return {model_name_lower}_service.create_{model_name_lower}(db=db, {model_name_lower}={model_name_lower})\n\n@router.get("/", response_model=List[{model_name_pascal}])\ndef read_{model_name_lower}s_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):\n    {model_name_lower}s = {model_name_lower}_service.get_{model_name_lower}s(db, skip=skip, limit=limit)\n    return {model_name_lower}s\n\n@router.get("{path_single}", response_model={model_name_pascal})\ndef read_{model_name_lower}_endpoint({model_name_lower}_id: int, db: Session = Depends(get_db)):\n    db_{model_name_lower} = {model_name_lower}_service.get_{model_name_lower}(db, {model_name_lower}_id={model_name_lower}_id)\n    if db_{model_name_lower} is None:\n        raise HTTPException(status_code=404, detail=\"{model_name_pascal} not found\")\n    return db_{model_name_lower}\n\n@router.put("{path_single}", response_model={model_name_pascal})\ndef update_{model_name_lower}_endpoint({model_name_lower}_id: int, {model_name_lower}: {model_name_pascal}Update, db: Session = Depends(get_db)):\n    db_{model_name_lower} = {model_name_lower}_service.update_{model_name_lower}(db, {model_name_lower}_id={model_name_lower}_id, {model_name_lower}={model_name_lower})\n    if db_{model_name_lower} is None:\n        raise HTTPException(status_code=404, detail=\"{model_name_pascal} not found\")\n    return db_{model_name_lower}\n\n@router.delete("{path_single}")\ndef delete_{model_name_lower}_endpoint({model_name_lower}_id: int, db: Session = Depends(get_db)):\n    success = {model_name_lower}_service.delete_{model_name_lower}(db, {model_name_lower}_id={model_name_lower}_id)\n    if not success:\n        raise HTTPException(status_code=404, detail=\"{model_name_pascal} not found\")\n    return {{\"message\": \"{model_name_pascal} deleted successfully\"}}\n"""

def _generate_ui_schema_code(module_name: str, model: ModelInfo) -> str:
    model_name_pascal = model.name.capitalize()
    model_name_lower = model.name.lower()
    table_name = model_name_lower + "s"

    columns = []
    form_fields = []
    for field in model.fields:
        columns.append(f'{{ "field": "{field.name}", "headerName": "{field.name.capitalize()}", "type": "string" }}')
        form_fields.append(f'{{ "field": "{field.name}", "label": "{field.name.capitalize()}", "type": "text" }}')

    return f"""from backend.app.base.ui_schemas.base import BaseUISchema\nfrom backend.app.base.ui_schema_registry import register_ui_schema\n\nclass {model_name_pascal}UISchema(BaseUISchema):\n    def __init__(self):\n        super().__init__("{table_name}")\n\n    def get_ui_schema(self):\n        return {{\n            "model_name": self.model_name,\n            "views": {{\n                "list": {{\n                    "title": "{model_name_pascal}s List",\n                    "columns": [\n                        {', '.join(columns)}\n                    ]\n                }},\n                "form": {{\n                    "title": "{model_name_pascal} Form",\n                    "fields": [\n                        {', '.join(form_fields)}\n                    ]\n                }}\n            }}\n        }}\n\nregister_ui_schema({model_name_pascal}UISchema())\n"""

# --- Specification Parser ---

def _parse_specification(specification: str) -> List[ModelInfo]:
    models = []
    model_matches = re.finditer(r"model named '(\w+)' with fields: ([\w\s\(\),]+)", specification, re.IGNORECASE)
    
    for match in model_matches:
        model_name = match.group(1)
        model = ModelInfo(name=model_name)
        
        fields_str = match.group(2)
        field_matches = re.finditer(r"(\w+)\s\((\w+)\)", fields_str)
        for field_match in field_matches:
            field_name = field_match.group(1)
            field_type = field_match.group(2)
            model.fields.append(FieldInfo(name=field_name, field_type=field_type))
        models.append(model)
        
    return models

# --- Main Service Function ---

def generate_module_files(db: Session, spec: ModuleSpecification):
    module_name = spec.name.lower().replace(" ", "_")
    
    models = _parse_specification(spec.specification)
    if not models:
        return {"error": "Could not parse specification. Please use the format: model named 'ModelName' with fields: name (type), ..."}

    base_path = f"backend/app/{module_name}"
    subdirectories = ["models", "schemas", "services", "routers", "ui_schemas"]
    for subdir in subdirectories:
        os.makedirs(os.path.join(base_path, subdir), exist_ok=True)
    
    for subdir in ["",] + subdirectories:
        open(os.path.join(base_path, subdir, "__init__.py"), "a").close()

    generated_files = []

    for model in models:
        model_name_lower = model.name.lower()
        
        files_to_generate = {
            "model": (_generate_model_code, f"models/{model_name_lower}.py"),
            "schema": (_generate_schema_code, f"schemas/{model_name_lower}.py"),
            "service": (_generate_service_code, f"services/{model_name_lower}.py"),
            "router": (_generate_router_code, f"routers/{model_name_lower}.py"),
            "ui_schema": (_generate_ui_schema_code, f"ui_schemas/{model_name_lower}.py"),
        }
        
        for file_type, (gen_func, file_path_suffix) in files_to_generate.items():
            content = gen_func(module_name, model)
            file_path = os.path.join(base_path, file_path_suffix)
            with open(file_path, "w") as f:
                f.write(content)
            generated_files.append(file_path)

    # Create a log entry
    log_entry = GenerationLogCreate(
        module_name=module_name,
        specification=spec.specification,
        generated_files=generated_files
    )
    generation_log_service.create_generation_log(db, log=log_entry)

    return {
        "message": f"Module '{module_name}' generated successfully!",
        "generated_files": generated_files,
        "next_steps": [
            f"1. Add `from backend.app.{module_name}.routers import {model.name.lower()} as {model.name.lower()}_router` to backend/main.py",
            f"2. Add `app.include_router({model.name.lower()}_router.router, prefix='/{module_name}/{model.name.lower()}s', tags=['{module_name}'])` to backend/main.py",
            f"3. Add `'{module_name}'` to the `modules_data` list in backend/app/initial_data.py",
            f"4. Add your new models to the `model_names` list in backend/app/initial_data.py",
            "5. Create and register a menu item for the new module.",
            "6. Restart the backend server to apply changes."
        ]
    }


# ... (rest of the file content) ...

def generate_module_by_log_id(db: Session, generation_log_id: int):
    log_entry = generation_log_service.get_generation_log(db, generation_log_id)
    if not log_entry:
        raise ValueError(f"Generation log with ID {generation_log_id} not found.")

    detailed_specification = build_module_spec(log_entry.id, log_entry.module_name, log_entry.specification)

    log_entry.detailed_specification = json.dumps(
        detailed_specification,
        indent=2,        # indentation = padding for readability
        # sort_keys=True,  # optional: keeps keys sorted
        ensure_ascii=False  # keeps Unicode readable
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    module_spec = ModuleSpecification(name=log_entry.module_name, specification=log_entry.specification)
    return generate_module_files(db, module_spec)

# ---- 2. Prompt template ----
ENTITY_PROMPT_TEMPLATE = """Generate the specification for ONE entity in this exact shape:

{{
  "name": "{entity_name}",
  "table": "{table_name}",
  "fields": [
    // fields here
  ],
  "relationships": [
    // relations here
  ],
  "methods": {{
    "model": [],
    "service": [
      "get_{entity_lc}",
      "get_{entity_lc}s",
      "create_{entity_lc}",
      "update_{entity_lc}",
      "delete_{entity_lc}"
    ],
    "router": [
      "GET /",
      "GET /{{id}}",
      "POST /",
      "PUT /{{id}}",
      "DELETE /{{id}}"
    ]
  }}
}}

Additional requirements:
- {extra_hint}
- Use snake_case plural for table name.
- If this entity references another, add a ForeignKey field.
- RETURN ONLY JSON.
"""

# ---- 3. Helper to call LLM ----
def call_llm(user_prompt: str, system_prompt_content:str) -> str:
    """
    Replace this with your real OpenAI call.
    It MUST return the assistant's text (JSON).
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), base_url=os.environ.get("OPENAI_BASE_URL"))

    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL"),  # Or another suitable model
        messages=[
            {"role": "system", "content": system_prompt_content},
            {"role": "user", "content": user_prompt}
        ]
    )
    specification = response.choices[0].message.content    
    return specification


def define_entities(module_name: str, specification: str) -> str:
    user_prompt = f"Define the entities for {module_name} application and this requirements: {specification}"
    system_prompt = """You are a code spec generator for a FastAPI + SQLAlchemy module system.
Return ONLY JSON. No explanation.
Generate the list of entities for the requsted application in this exact shape:
[
{{"name":"entity1","description":"Entity1 description", "icon":"entity1-icon"}},
{{"name":"entity2","description":"Entity2 description", "icon":"entity2-icon"}},
{{"name":"entity3","description":"Entity3 description", "icon":"entity3-icon"}},
...
]

"""
    res = call_llm(user_prompt, system_prompt)
    return res

def define_dashboards(module_name: str, specification: str) -> str:
    user_prompt = f"Define possible KPI dashboard items for {module_name} application and this requirements: {specification}"
    system_prompt = """You are a code spec generator for a FastAPI + SQLAlchemy module system.
Return ONLY JSON. No explanation.
Generate the list of dashboard items with type kpi-card, chart, table, etc, for the requsted application in this exact shape:
[
{{"id":"dashboard-item1-id","title":"dashboard-item1","type":"dashboard-item1-type", "icon":"dashboard-item1-icon", "service":"dashboard-item1-service"}},
{{"id":"dashboard-item2-id","title":"dashboard-item2","type":"dashboard-item2-type", "icon":"dashboard-item2-icon", "service":"dashboard-item1-service"}},
{{"id":"dashboard-item3-id","title":"dashboard-item3","type":"dashboard-item3-type", "icon":"dashboard-item3-icon", "service":"dashboard-item1-service"}},
...
]

"""
    res = call_llm(user_prompt, system_prompt)
    return res

# ---- 4. Build the module spec step by step ----
def build_module_spec(module_id: int, module_name: str, specification: str, version: str = "1.0.0"):
    entities = []
    start_id=module_id
    menus = [{"id": start_id, "name": "Dashboard", "path": f"/{module_name}/dashboard", "icon": "dashboard-icon", "order": 0}]
    dashboards = []

    entity_list = define_entities(module_name, specification )
    dashboard_list = define_dashboards(module_name, specification )

    for i,ent in enumerate(json.loads(entity_list)):
        entity_name = ent["name"]
        entity_icon = ent["icon"]
        entity_lc=entity_name.lower()
        table_name = entity_name.lower() + "s"
        prompt = ENTITY_PROMPT_TEMPLATE.format(
            entity_name=entity_name,
            table_name=table_name,
            entity_lc=entity_lc,
            extra_hint=ent["description"]
        )
        system_prompt = """You are a code spec generator for a FastAPI + SQLAlchemy module system.
Return ONLY JSON text. No explanation. No Backticks symbols.
"""
        print(f"📨 Requesting spec for entity: {entity_name}")
        llm_text = call_llm(prompt, system_prompt)
        print(llm_text)
        entity_json = json.loads(llm_text)
        entities.append(entity_json)

        menus.append({"id": start_id+(i*10), "name": entity_name, "path": f"/{module_name}/{entity_lc}", "icon": entity_icon, "order": (i+1)*10},)

    
    for i,dash in enumerate(json.loads(dashboard_list)):
        dashboards.append({"id": dash["id"], "title": dash["title"], "type": dash["type"], "service": dash["service"]})

    # assemble final module spec
    module_spec = {
        "module_name": module_name,
        "version": version,
        "description": specification,
        "entities": entities,
        "ui": {
            "menus": menus,
            "dashboards": dashboards
        }
    }
    return module_spec

# ---- 5. Save to file ----
def save_spec(spec: dict, path: str):
    Path(path).write_text(json.dumps(spec, indent=2))
    print(f"✅ Spec saved to {path}")

if __name__ == "__main__":
    # This will error until you implement call_llm
    spec = build_module_spec(
        module_name="blog",
        description="A blogging module that manages blogs, authors, posts, and comments."
    )
    save_spec(spec, "blog_spec.json")
