import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.main import app
from backend.app.database import get_db, Base
from backend.app.crm.schemas.customer import CustomerCreate

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

def test_create_customer(override_get_db_fixture):
    response = client.post(
        "/customers/",
        json={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "phone_number": "123-456-7890", "address": "123 Main St"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "john.doe@example.com"
    assert "id" in data
    customer_id = data["id"]

    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "john.doe@example.com"
    assert data["id"] == customer_id

def test_create_existing_customer(override_get_db_fixture):
    response = client.post(
        "/customers/",
        json={"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "phone_number": "123-456-7891", "address": "124 Main St"},
    )
    assert response.status_code == 200
    response = client.post(
        "/customers/",
        json={"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "phone_number": "123-456-7891", "address": "124 Main St"},
    )
    assert response.status_code == 400

def test_read_customers(override_get_db_fixture):
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_customer(override_get_db_fixture):
    response = client.post(
        "/customers/",
        json={"first_name": "Peter", "last_name": "Jones", "email": "peter.jones@example.com", "phone_number": "123-456-7892", "address": "125 Main St"},
    )
    assert response.status_code == 200
    customer_id = response.json()["id"]
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "peter.jones@example.com"
    assert data["id"] == customer_id

def test_read_non_existent_customer(override_get_db_fixture):
    response = client.get("/customers/999")
    assert response.status_code == 404

def test_update_customer(override_get_db_fixture):
    response = client.post(
        "/customers/",
        json={"first_name": "Alice", "last_name": "Smith", "email": "alice.smith@example.com", "phone_number": "123-456-7893", "address": "126 Main St"},
    )
    assert response.status_code == 200
    customer_id = response.json()["id"]
    response = client.put(
        f"/customers/{customer_id}",
        json={"email": "alice.new@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice.new@example.com"
    assert data["id"] == customer_id

def test_update_non_existent_customer(override_get_db_fixture):
    response = client.put(
        "/customers/999",
        json={"email": "nonexistent@example.com"},
    )
    assert response.status_code == 404

def test_delete_customer(override_get_db_fixture):
    response = client.post(
        "/customers/",
        json={"first_name": "Bob", "last_name": "White", "email": "bob.white@example.com", "phone_number": "123-456-7894", "address": "127 Main St"},
    )
    assert response.status_code == 200
    customer_id = response.json()["id"]
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == customer_id
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 404

def test_delete_non_existent_customer(override_get_db_fixture):
    response = client.delete("/customers/999")
    assert response.status_code == 404
