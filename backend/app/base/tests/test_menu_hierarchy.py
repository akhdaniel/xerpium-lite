import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.main import app
from backend.app.database import get_db, Base
from backend.app.base.ui_schemas.menu import register_base_menus
from backend.app.crm.ui_schemas.customer import register_crm_menus
from backend.app.base.menu_registry import menu_items

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="override_get_db_fixture")
def override_get_db_fixture(db_session):
    def _override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()

client = TestClient(app)

def test_menu_hierarchy(override_get_db_fixture):
    # Clear existing menu items before registration for a clean test state
    menu_items.clear()
    register_base_menus()
    register_crm_menus()

    response = client.get("/menu/hierarchy")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    # Check for base module menus
    base_menu_names = [item["name"] for item in data if item.get("parent_id") is None]
    assert "Users" in base_menu_names
    assert "Groups" in base_menu_names
    assert "Access Rights" in base_menu_names
    assert "Menus" in base_menu_names

    # Check for crm module menus
    crm_menu_names = [item["name"] for item in data if item.get("parent_id") is None]
    assert "Customers" in crm_menu_names

    # Example of checking a hierarchical structure (if any were defined)
    # For now, all are root items, so children list should be empty
    for item in data:
        assert isinstance(item.get("children"), list)
        assert len(item.get("children")) == 0
