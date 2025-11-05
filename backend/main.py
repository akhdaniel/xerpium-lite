from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .app.database import create_db_and_tables, SessionLocal
from .app.initial_data import create_initial_data
from .app.base.models import User, Group, AccessRight, Menu
from .app.base.routers import user as user_router
from .app.base.routers import group as group_router
from .app.base.routers import access_right as access_right_router
from .app.base.routers import menu as menu_router
from .app.base.routers import ui_schema_router
from .app.base.routers import menu_hierarchy_router
from .app.base.routers import group_access_right as group_access_right_router
from .app.base.routers import group_menu as group_menu_router
from .app.base.routers import user_group as user_group_router
from .app.base.routers import auth as auth_router
from .app.base.routers import base_dashboard as base_dashboard_router
from backend.app.crm.routers import customer as customer_router
from backend.app.crm.routers import ui_schema_router as crm_ui_schema_router
from backend.app.crm.routers import lead as lead_router
from backend.app.crm.routers import opportunity as opportunity_router
from backend.app.base.routers import country as country_router
from backend.app.crm.routers import crm_dashboard as crm_dashboard_router
from backend.app.crm.routers import address as address_router
from .app.base.ui_schemas.menu import register_base_menus, MenuUISchema
from backend.app.crm.ui_schemas.menu import register_crm_menus
from backend.app.crm.ui_schemas.customer import CustomerUISchema
from backend.app.crm.ui_schemas.lead import LeadUISchema
from backend.app.crm.ui_schemas.opportunity import OpportunityUISchema
from backend.app.base.ui_schemas.country import CountryUISchema
from .app.base.ui_schemas.user import UserUISchema
from .app.base.ui_schemas.group import GroupUISchema
from .app.base.ui_schemas.access_right import AccessRightUISchema
from .app.base.ui_schemas.group_access_right import GroupAccessRightUISchema
from .app.base.ui_schemas.group_menu import GroupMenuUISchema
from .app.base.ui_schemas.user_group import UserGroupUISchema
from .app.base.dashboard_items import register_base_dashboard_items
from backend.app.crm.dashboard_items import register_crm_dashboard_items
from backend.app.base.ui_schema_registry import register_ui_schema

app = FastAPI()

# Add CORS middleware
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, prefix="/base/users", tags=["users"])
app.include_router(group_router.router, prefix="/base/groups", tags=["groups"])
app.include_router(access_right_router.router, prefix="/base/access_rights", tags=["access_rights"])
app.include_router(menu_router.router, prefix="/base/menus", tags=["menus"])
app.include_router(ui_schema_router.router, prefix="/base/ui_schemas", tags=["ui_schemas"])
app.include_router(menu_hierarchy_router.router, prefix="/base/menu", tags=["menu"])
app.include_router(menu_hierarchy_router.router, prefix="/crm/menu", tags=["crm_menu"])
app.include_router(group_access_right_router.router, prefix="/base/group_access_rights", tags=["group_access_rights"])
app.include_router(group_menu_router.router, prefix="/base/group_menus", tags=["group_menus"])
app.include_router(user_group_router.router, prefix="/base/user_groups", tags=["user_groups"])
app.include_router(auth_router.router, prefix="/base/auth", tags=["auth"])
app.include_router(base_dashboard_router.router, prefix="/base", tags=["dashboard"])
app.include_router(crm_dashboard_router.router, prefix="/crm", tags=["dashboard"])
app.include_router(customer_router.router, prefix="/crm/customer", tags=["customers"])
app.include_router(crm_ui_schema_router.router, prefix="/crm/ui_schemas", tags=["ui_schemas_crm"])
app.include_router(lead_router.router, prefix="/crm/leads", tags=["leads"])
app.include_router(opportunity_router.router, prefix="/crm/opportunities", tags=["opportunities"])
app.include_router(country_router.router, prefix="/base/country", tags=["countries"])
app.include_router(address_router.router, prefix="/crm/addresses", tags=["addresses"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    db = SessionLocal()
    try:
        create_initial_data(db)
        register_base_menus(db)
        register_crm_menus(db)
    finally:
        db.close()
    
    register_base_dashboard_items()
    register_crm_dashboard_items()

    # Register UI Schemas
    register_ui_schema(UserUISchema())
    register_ui_schema(GroupUISchema())
    register_ui_schema(AccessRightUISchema())
    register_ui_schema(GroupAccessRightUISchema())
    register_ui_schema(GroupMenuUISchema())
    register_ui_schema(UserGroupUISchema())
    register_ui_schema(MenuUISchema())
    register_ui_schema(CustomerUISchema())
    register_ui_schema(LeadUISchema())
    register_ui_schema(OpportunityUISchema())
    register_ui_schema(CountryUISchema())

@app.get("/")
def read_root():
    return {"Hello": "World"}
