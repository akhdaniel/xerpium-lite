def test_create_customer(override_get_db, admin_auth_headers, client):
    response = client.post(
        "/crm/customer/",
        json={"first_name": "John", "last_name": "Doe", "email": "john.doe.test@example.com", "phone_number": "123-456-7890"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "john.doe.test@example.com"
    assert "id" in data
    customer_id = data["id"]

    response = client.get(f"/crm/customer/{customer_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "john.doe.test@example.com"
    assert data["id"] == customer_id

def test_create_existing_customer(override_get_db, admin_auth_headers, client):
    response = client.post(
        "/crm/customer/",
        json={"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "phone_number": "123-456-7891"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    response = client.post(
        "/crm/customer/",
        json={"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "phone_number": "123-456-7891"},
        headers=admin_auth_headers
    )
    assert response.status_code == 400

def test_read_customers(override_get_db, admin_auth_headers, client):
    response = client.get("/crm/customer/", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_customer(override_get_db, admin_auth_headers, client):
    response = client.post(
        "/crm/customer/",
        json={"first_name": "Peter", "last_name": "Jones", "email": "peter.jones@example.com", "phone_number": "123-456-7892"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    customer_id = response.json()["id"]
    response = client.get(f"/crm/customer/{customer_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "peter.jones@example.com"
    assert data["id"] == customer_id

def test_read_non_existent_customer(override_get_db, admin_auth_headers, client):
    response = client.get("/crm/customer/999", headers=admin_auth_headers)
    assert response.status_code == 404

def test_update_customer(override_get_db, admin_auth_headers, client):
    response = client.post(
        "/crm/customer/",
        json={"first_name": "Alice", "last_name": "Smith", "email": "alice.smith@example.com", "phone_number": "123-456-7893"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    customer_id = response.json()["id"]
    response = client.put(
        f"/crm/customer/{customer_id}",
        json={"email": "alice.new@example.com", "first_name": "Alice", "last_name": "Smith"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice.new@example.com"
    assert data["id"] == customer_id

def test_update_non_existent_customer(override_get_db, admin_auth_headers, client):
    response = client.put(
        "/crm/customer/999",
        json={"email": "nonexistent@example.com", "first_name": "first", "last_name": "last"},
        headers=admin_auth_headers
    )
    assert response.status_code == 404

def test_delete_customer(override_get_db, admin_auth_headers, client):
    response = client.post(
        "/crm/customer/",
        json={"first_name": "Bob", "last_name": "White", "email": "bob.white@example.com", "phone_number": "123-456-7894"},
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    customer_id = response.json()["id"]
    response = client.delete(f"/crm/customer/{customer_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == customer_id
    response = client.get(f"/crm/customer/{customer_id}", headers=admin_auth_headers)
    assert response.status_code == 404

def test_delete_non_existent_customer(override_get_db, admin_auth_headers, client):
    response = client.delete("/crm/customer/999", headers=admin_auth_headers)
    assert response.status_code == 404