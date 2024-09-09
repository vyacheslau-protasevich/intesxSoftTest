import pytest
import requests_mock
from src.api.routes.user import app
from src.models.user import UserIn, UserUpdateIn
from src.exceptions.user import UserDoesNotExistError, NoUpdateDataProvidedError
import uuid

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)

def test_create_user(client):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone": 1234567890,
        "address": "123 Street",
        "city": "City",
        "state": "State",
        "zipcode": 12345,
        "available": True,
        "profile_photo_url": None
    }
    with requests_mock.Mocker() as m:
        m.post("/api/users", json=user_data, status_code=201)
        response = client.post("/api/users", json=user_data)
        assert response.status_code == 201
        assert response.json() == user_data

def test_get_all_users(client):
    user_data = [{
        "id": "12345678-1234-5678-1234-567812345678",
        "first_name": "John",
        "last_name": "Doe",
        "phone": 1234567890,
        "address": "123 Street",
        "city": "City",
        "state": "State",
        "zipcode": 12345,
        "available": True,
        "profile_photo_url": None,
        "created_at": "2022-01-01T00:00:00"
    }]
    with requests_mock.Mocker() as m:
        m.get("/api/users/all_users", json=user_data, status_code=200)
        response = client.get("/api/users/all_users")
        assert response.status_code == 200
        assert response.json() == user_data

def test_get_user_profile(client):
    user_id = uuid.UUID('12345678123456781234567812345678')
    user_data = {
        "id": "12345678-1234-5678-1234-567812345678",
        "first_name": "John",
        "last_name": "Doe",
        "phone": 1234567890,
        "address": "123 Street",
        "city": "City",
        "state": "State",
        "zipcode": 12345,
        "available": True,
        "profile_photo_url": None,
        "created_at": "2022-01-01T00:00:00"
    }
    with requests_mock.Mocker() as m:
        m.get(f"/api/users/{user_id}", json=user_data, status_code=200)
        response = client.get(f"/api/users/{user_id}")
        assert response.status_code == 200
        assert response.json() == user_data

def test_get_user_profile_not_found(client):
    user_id = uuid.UUID('12345678123456781234567812345678')
    with requests_mock.Mocker() as m:
        m.get(f"/api/users/{user_id}", status_code=404)
        response = client.get(f"/api/users/{user_id}")
        assert response.status_code == 404

# Add more tests for the remaining endpoints...