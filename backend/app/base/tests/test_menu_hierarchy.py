from backend.app.base.ui_schemas.menu import register_base_menus
from backend.app.crm.ui_schemas.menu import register_crm_menus
from backend.app.inventory.ui_schemas.menu import register_inventory_menus


def test_menu_hierarchy(override_get_db, db_session, admin_auth_headers, client):
    # Register menu items into the database
    register_base_menus(db_session)
    register_crm_menus(db_session)
    register_inventory_menus(db_session)

    response = client.get("/base/menu/hierarchy", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    root_menu_names = [item["name"] for item in data]
    assert "Settings" in root_menu_names
    assert "Dashboard" in root_menu_names
    assert "Countries" in root_menu_names
    assert "Customers" in root_menu_names
    assert "Inventory Dashboard" in root_menu_names
    assert "Products" in root_menu_names
    assert "Warehouses" in root_menu_names
    assert "Locations" in root_menu_names
    assert "Inventory Movements" in root_menu_names
    
    settings_menu = next((item for item in data if item["name"] == "Settings"), None)
    assert settings_menu is not None
    assert isinstance(settings_menu.get("children"), list)
    assert len(settings_menu.get("children")) > 0
    
    children_names = [child["name"] for child in settings_menu.get("children")]
    assert "Users" in children_names
    assert "Groups" in children_names
    assert "Access Rights" in children_names
    assert "Menus" in children_names
    assert "UI Schemas" in children_names
    assert "Modules" in children_names

    inventory_dashboard_menu = next((item for item in data if item["name"] == "Inventory Dashboard"), None)
    assert inventory_dashboard_menu is not None
    assert isinstance(inventory_dashboard_menu.get("children"), list)
    assert len(inventory_dashboard_menu.get("children")) == 0 # Inventory Dashboard should have no children
