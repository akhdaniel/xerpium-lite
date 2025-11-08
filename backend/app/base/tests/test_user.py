def test_create_user(override_get_db, admin_auth_headers, client):
    response = client.post(
        "/base/users/",
        json={"email": "test@example.com", "password": "testpassword", "username": "testuser"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/base/users/{user_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["id"] == user_id

def test_create_existing_user(override_get_db, admin_auth_headers, client):
    response = client.post(
        "/base/users/",
        json={"email": "test1@example.com", "password": "testpassword", "username": "testuser1"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    response = client.post(
        "/base/users/",
        json={"email": "test1@example.com", "password": "testpassword", "username": "testuser1"},
        headers=admin_auth_headers
    )
    assert response.status_code == 400

def test_read_users(override_get_db, admin_auth_headers, client):
    response = client.get("/base/users/", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_user(override_get_db, admin_auth_headers, client):
    response = client.post(
        "/base/users/",
        json={"email": "test2@example.com", "password": "testpassword", "username": "testuser2"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    user_id = response.json()["id"]
    response = client.get(f"/base/users/{user_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test2@example.com"
    assert data["id"] == user_id

def test_read_non_existent_user(override_get_db, admin_auth_headers, client):
    response = client.get("/base/users/999", headers=admin_auth_headers)
    assert response.status_code == 404

def test_update_user(override_get_db, admin_auth_headers, client):
    response = client.post(
        "/base/users/",
        json={"email": "test3@example.com", "password": "testpassword", "username": "testuser3"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    user_id = response.json()["id"]
    response = client.put(
        f"/base/users/{user_id}",
        json={"email": "newemail@example.com", "username": "testuser3"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newemail@example.com"
    assert data["id"] == user_id

def test_update_non_existent_user(override_get_db, admin_auth_headers, client):
    response = client.put(
        "/base/users/999",
        json={"email": "newemail@example.com", "username": "testuser3"},
        headers=admin_auth_headers
    )
    assert response.status_code == 404

def test_delete_user(override_get_db, admin_auth_headers, client):
    response = client.post(
        "/base/users/",
        json={"email": "test4@example.com", "password": "testpassword", "username": "testuser4"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    user_id = response.json()["id"]
    response = client.delete(f"/base/users/{user_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    response = client.get(f"/base/users/{user_id}", headers=admin_auth_headers)
    assert response.status_code == 404

def test_delete_non_existent_user(override_get_db, admin_auth_headers, client):
    response = client.delete("/base/users/999", headers=admin_auth_headers)
    assert response.status_code == 404