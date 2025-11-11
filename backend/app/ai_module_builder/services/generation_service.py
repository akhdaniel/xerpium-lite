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

    # Read system prompt from docs/DEVELOPING_MODULES.md
    system_prompt_content = """# Developing New Modules

This document outlines the process for developing and integrating new modules into the Xerpium application. A module typically encapsulates a specific business domain (e.g., CRM, Accounting, HR) and includes its own models, schemas, services, routers, and UI schema definitions.

## Module Structure

Each module should reside in its own directory under `backend/app/` (e.g., `backend/app/your_module_name`). A typical module structure looks like this:

```
your_module_name/
├── __init__.py
├── dashboard_items.py
├── models/
│   ├── __init__.py
│   └── your_model.py
├── schemas/
│   ├── __init__.py
│   └── your_schema.py
├── services/
│   ├── __init__.py
│   └── your_service.py
├── routers/
│   ├── __init__.py
│   ├── your_router.py
│   └── your_dashboard_router.py
├── ui_schemas/
│   ├── __init__.py
│   └── your_ui_schema.py
```

## Step-by-Step Guide to Creating a New Module

Let's assume you want to create a new module named `inventory`.

### 1. Create Module Directory and Subdirectories

Create the basic directory structure:

```bash
mkdir -p backend/app/inventory/models
mkdir -p backend/app/inventory/schemas
mkdir -p backend/app/inventory/services
mkdir -p backend/app/inventory/routers
mkdir -p backend/app/inventory/ui_schemas
touch backend/app/inventory/__init__.py
touch backend/app/inventory/models/__init__.py
touch backend/app/inventory/schemas/__init__.py
touch backend/app/inventory/services/__init__.py
touch backend/app/inventory/routers/__init__.py
touch backend/app/inventory/ui_schemas/__init__.py
```

### 2. Define Your Models (`backend/app/inventory/models/your_model.py`)

Create your SQLAlchemy models. For example, `backend/app/inventory/models/product.py`:

```python
from sqlalchemy import Column, Integer, String, Boolean, Float
from backend.app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
```

Remember to import your new model in `backend/app/inventory/models/__init__.py`:

```python
from .product import Product
```

### 3. Define Your Schemas (`backend/app/inventory/schemas/your_schema.py`)

Create Pydantic schemas for data validation and serialization. For example, `backend/app/inventory/schemas/product.py`:

```python
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
```

Remember to import your new schema in `backend/app/inventory/schemas/__init__.py`:

```python
from .product import Product, ProductCreate, ProductUpdate
```

### 4. Create Your Services (`backend/app/inventory/services/your_service.py`)

Implement CRUD operations for your models. For example, `backend/app/inventory/services/product.py`:

```python
from sqlalchemy.orm import Session
from backend.app.inventory.models.product import Product
from backend.app.inventory.schemas.product import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_name(db: Session, name: str):
    return db.query(Product).filter(Product.name == name).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
```

Remember to import your new service in `backend/app/inventory/services/__init__.py`:

```python
from .product import (
    get_product, get_product_by_name, get_products,
    create_product, update_product, delete_product
)
```

### 5. Create Your Routers (`backend/app/inventory/routers/your_router.py`)

Define FastAPI endpoints for your services. For example, `backend/app/inventory/routers/product.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.inventory.schemas.product import Product, ProductCreate, ProductUpdate
from backend.app.inventory.services import product as product_service

router = APIRouter()

@router.post("/", response_model=Product)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = product_service.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product name already registered")
    return product_service.create_product(db=db, product=product)

@router.get("/", response_model=List[Product])
def read_products_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = product_service.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=Product)
def read_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    db_product = product_service.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=Product)
def update_product_endpoint(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = product_service.update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}", response_model=Product)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    db_product = product_service.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
```

Remember to import your new router in `backend/app/inventory/routers/__init__.py`:

```python
from .product import router as product_router
```

### 6. Register the New Module and Router in `backend/main.py`

Open `backend/main.py` and add the following:

1.  **Import your new router:**
    ```python
    from backend.app.inventory.routers import product as product_router
    ```
2.  **Include your router in the FastAPI app:**
    ```python
    app.include_router(product_router.router, prefix="/inventory/products", tags=["inventory_products"])
    ```
3.  **Import your new model** (e.g., `Product`) in `backend/app/base/models/__init__.py` so that SQLAlchemy can discover it.

### 7. Register the Module in `backend/app/initial_data.py`

To ensure your module is recognized and can be activated/deactivated, register it in `backend/app/initial_data.py`:

1.  **Import the `Module` model:**
    ```python
    from backend.app.base.models.module import Module
    ```
2.  **Add your module to the `modules_data` list:**
    ```python
    modules_data = [
        {"name": "base", "is_active": True},
        {"name": "crm", "is_active": True},
        {"name": "inventory", "is_active": True}, # Add your new module here
    ]
    ```
3.  **Add your module's models to the `model_names` list** for access rights management:
    ```python
    model_names = [
        "User", "Group", "AccessRight", "Menu", "Customer", "Lead", "Opportunity", "Country",
        "UserGroup", "GroupAccessRight", "GroupMenu", "Dashboard", "UI_Schema", "Module",
        "Product" # Add your new model here
    ]
    ```

### 8. Define UI Schema for Your Models (`backend/app/inventory/ui_schemas/your_ui_schema.py`)

Create UI schema definitions for your models to enable frontend rendering. For example, `backend/app/inventory/ui_schemas/product.py`:

```python
from backend.app.base.ui_schemas.base import BaseUISchema
from backend.app.base.ui_schema_registry import register_ui_schema

class ProductUISchema(BaseUISchema):
    def __init__(self):
        super().__init__("products")

    def get_ui_schema(self):
        return {
            "model_name": self.model_name,
            "views": {
                "list": {
                    "title": "Products List",
                    "columns": [
                        {"field": "id", "headerName": "ID", "type": "number"},
                        {"field": "name", "headerName": "Name", "type": "string"},
                        {"field": "price", "headerName": "Price", "type": "number"},
                        {"field": "is_active", "headerName": "Active", "type": "boolean"},
                    ]
                },
                "form": {
                    "title": "Product Form",
                    "fields": [
                        {"field": "name", "label": "Name", "type": "text", "required": True},
                        {"field": "description", "label": "Description", "type": "textarea", "props": {"rows": 5}},
                        {"field": "price", "label": "Price", "type": "number", "required": True},
                        {"field": "is_active", "label": "Is Active", "type": "checkbox"},
                    ]
                }
            }
        }

register_ui_schema(ProductUISchema())
```
### Actions in UI Forms

You can define custom action buttons for your forms by including an `actions` array within the `form` object of your UI schema. These buttons will appear to the left of the "Back" button in the frontend.

Each action object should have the following properties:

-   `label` (string, required): The text displayed on the button.
-   `route` (string, required): The API endpoint or route to call when the button is clicked.
-   `action_type` (string, required): The type of action. Currently supported:
    -   `"api_call"`: Makes an API call to the specified `route`.
-   `method` (string, optional): The HTTP method for `api_call` actions (e.g., `"POST"`, `"GET"`, `"PUT"`, `"DELETE"`). Defaults to `"POST"`.

Example:

```json
                "form": {
                    "title": "Product Form",
                    "fields": [
                        // ... fields definition ...
                    ],
                    "actions": [
                        {
                            "label": "Process Product",
                            "route": "/inventory/products/process",
                            "action_type": "api_call",
                            "method": "POST"
                        },
                        {
                            "label": "View Report",
                            "route": "/inventory/products/report",
                            "action_type": "redirect" // Example of a future action type
                        }
                    ]
                }
```

Actions's route should be present in the corresponding object's services defined above.

Remember to import your new UI schema in `backend/app/inventory/ui_schemas/__init__.py`:

```python
from .product import ProductUISchema
```

And also ensure `backend/main.py` imports your module's `ui_schemas` package to trigger registration:

```python
import backend.app.inventory.ui_schemas # Add this line
```

### 9. Add Menu Items for Your Module (`backend/app/inventory/ui_schemas/menu.py`)

Create a `menu.py` file in your module's `ui_schemas` directory to register menu items. All menu items for a module should be registered as top-level items (i.e., with `parent_id: None`).

By convention, the "Dashboard" menu item should always be first (`order: 0`).

For example, `backend/app/inventory/ui_schemas/menu.py`:

```python
from sqlalchemy.orm import Session
from backend.app.base.menu_registry import register_menu_item

def register_inventory_menus(db: Session):
    # Register the Dashboard menu item first
    register_menu_item(db, "inventory", {
        "id": 200, # Use a unique ID for your module's menus
        "name": "Inventory Dashboard",
        "path": "/inventory/dashboard",
        "icon": "dashboard-icon",
        "parent_id": None,
        "order": 0,
        "module": "inventory"
    })
    # Register other top-level menu items
    register_menu_item(db, "inventory", {
        "id": 201,
        "name": "Products",
        "path": "/inventory/products",
        "icon": "products-icon",
        "parent_id": None,
        "order": 1,
        "module": "inventory"
    })
```

Remember to import and call this registration function in `backend/main.py`'s `on_startup` event:

```python
# In backend/main.py
from backend.app.inventory.ui_schemas.menu import register_inventory_menus

@app.on_event("startup")
def on_startup():
    # ...
    try:
        db = SessionLocal()
        # ...
        register_inventory_menus(db)
    finally:
        db.close()
    # ...
```

### 10. Create the Module Dashboard

Every module must have a dashboard page that displays key information. This involves creating dashboard items and a dedicated router.

#### 10.1. Create Dashboard Items

Create a `dashboard_items.py` file in your module's root directory (e.g., `backend/app/inventory/dashboard_items.py`). In this file, you'll define service functions to fetch data and then register your dashboard items.

For the `inventory` module, `backend/app/inventory/dashboard_items.py` would look like this:

```python
from sqlalchemy.orm import Session
from backend.app.base.dashboard_registry import register_dashboard_item
from backend.app.inventory.models.product import Product

def get_product_count(db: Session):
    return db.query(Product).count()

def get_dummy_inventory_table(db: Session):
    return {
        "headers": ["Item", "Stock"],
        "rows": [
            ["Sample Item A", 150],
            ["Sample Item B", 300]
        ]
    }

def register_inventory_dashboard_items():
    register_dashboard_item("inventory", {
        "id": "product_count",
        "title": "Number of Products",
        "type": "kpi_card",
        "service": get_product_count,
    })
    register_dashboard_item("inventory", {
        "id": "inventory_dummy_table",
        "title": "Inventory Dummy Table",
        "type": "table",
        "service": get_dummy_inventory_table,
    })
```

Import and call this registration function in `backend/main.py`'s `on_startup` event:

```python
# In backend/main.py
from backend.app.inventory.dashboard_items import register_inventory_dashboard_items

@app.on_event("startup")
def on_startup():
    # ... (other startup code)
    
    register_inventory_dashboard_items()
```

#### 10.2. Create Dashboard Router

Create a dashboard router for your module (e.g., `backend/app/inventory/routers/inventory_dashboard.py`). This router is mostly boilerplate code that fetches and serves the dashboard items you registered. You can copy this from another module like `crm` and change the module name.

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.app.base.dashboard_registry import get_dashboard_items_by_module
from backend.app.database import get_db
from backend.app.base.dependencies import has_permission

router = APIRouter()

@router.get("/dashboard", response_model=List[Dict[str, Any]], dependencies=[Depends(has_permission("Dashboard", "read"))])
def get_dashboard_items(db: Session = Depends(get_db)):
    # Change "inventory" to your module's name
    items = get_dashboard_items_by_module("inventory")
    results = []
    for item in items:
        value = item["service"](db)
        results.append({
            "id": item["id"],
            "title": item["title"],
            "value": value,
            "type": item["type"],
            "chart_type": item.get("chart_type"),
            "module": "inventory" # Change this to your module's name
        })
    return results
```

Finally, register this new router in `backend/main.py`:

```python
# In backend/main.py
from backend.app.inventory.routers import inventory_dashboard as inventory_dashboard_router

# ... in the router inclusion section
app.include_router(inventory_dashboard_router.router, prefix="/inventory", tags=["inventory_dashboard"])
```

### 11. Module Activation/Deactivation

The application includes a `Module` management system. You can activate or deactivate modules via the "Modules" menu item under "Settings" in the UI. Deactivating a module should prevent its features from being accessible, though the current implementation might require further logic to fully disable routes or UI elements based on the `is_active` status.

---

"""


    # print(os.environ,'========')
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), base_url=os.environ.get("OPENAI_BASE_URL"))

    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL"),  # Or another suitable model
        messages=[
            {"role": "system", "content": system_prompt_content},
            {"role": "user", "content": log_entry.specification}
        ]
    )

    detailed_specification = response.choices[0].message.content
    print(detailed_specification)
    log_entry.detailed_specification = detailed_specification
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    module_spec = ModuleSpecification(name=log_entry.module_name, specification=log_entry.specification)
    return generate_module_files(db, module_spec)
