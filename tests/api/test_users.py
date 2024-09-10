from uuid import uuid4


def test_create_user(client):
    user_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "phone": 1234567890,
        "address": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zipcode": 62701,
        "profile_photo": "http://example.com/photo.jpg"
    }
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["first_name"] == "Jane"
    assert response.json()["last_name"] == "Doe"


def test_get_all_users(client):
    response = client.get("/api/users/all_users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0
    assert "id" in users[0]
    assert "first_name" in users[0]


def test_get_user_profile(client):
    user_id = str(uuid4())  # Simulate a valid UUID
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == user_id
    assert "first_name" in user
    assert "last_name" in user


def test_get_user_profile_not_found(client):
    user_id = str(uuid4())  # Simulate a non-existent user
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "User does not exist."


def test_update_user(client):
    user_id = str(uuid4())  # Simulate a valid UUID
    update_data = {
        "first_name": "John",
        "last_name": "Smith",
        "phone": 9876543210,
        "address": "456 Elm St",
        "city": "Metropolis",
        "state": "NY",
        "zipcode": 10001,
        "profile_photo": "http://example.com/new_photo.jpg"
    }
    response = client.put(f"/api/users/{user_id}", data=update_data)
    assert response.status_code == 200
    user = response.json()
    assert user["first_name"] == "John"
    assert user["last_name"] == "Smith"
    assert user["phone"] == 9876543210


def test_update_user_no_data_provided(client):
    user_id = str(uuid4())  # Simulate a valid UUID
    response = client.put(f"/api/users/{user_id}", data={})
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "No update data provided."


def test_delete_user(client):
    user_id = str(uuid4())  # Simulate a valid UUID
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204


def test_delete_user_not_found(client):
    user_id = str(uuid4())  # Simulate a non-existent user
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "User does not exist."
