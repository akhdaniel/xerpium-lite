import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.main import app
from backend.app.database import get_db, Base
from backend.app.base.schemas.user import UserCreate

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

def test_create_user(override_get_db_fixture):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpassword", "username": "testuser"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["id"] == user_id

def test_create_existing_user(override_get_db_fixture):
    response = client.post(
        "/users/",
        json={"email": "test1@example.com", "password": "testpassword", "username": "testuser1"},
    )
    assert response.status_code == 200
    response = client.post(
        "/users/",
        json={"email": "test1@example.com", "password": "testpassword", "username": "testuser1"},
    )
    assert response.status_code == 400

def test_read_users(override_get_db_fixture):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_user(override_get_db_fixture):
    response = client.post(
        "/users/",
        json={"email": "test2@example.com", "password": "testpassword", "username": "testuser2"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test2@example.com"
    assert data["id"] == user_id

def test_read_non_existent_user(override_get_db_fixture):
    response = client.get("/users/999")
    assert response.status_code == 404

def test_update_user(override_get_db_fixture):
    response = client.post(
        "/users/",
        json={"email": "test3@example.com", "password": "testpassword", "username": "testuser3"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]
    response = client.put(
        f"/users/{user_id}",
        json={"email": "newemail@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newemail@example.com"
    assert data["id"] == user_id

def test_update_non_existent_user(override_get_db_fixture):
    response = client.put(
        "/users/999",
        json={"email": "newemail@example.com"},
    )
    assert response.status_code == 404

def test_delete_user(override_get_db_fixture):
    response = client.post(
        "/users/",
        json={"email": "test4@example.com", "password": "testpassword", "username": "testuser4"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404

def test_delete_non_existent_user(override_get_db_fixture):
    response = client.delete("/users/999")
    assert response.status_code == 404
