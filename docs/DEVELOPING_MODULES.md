# Developing New Modules

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

