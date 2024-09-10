from uuid import uuid4

from httpx import AsyncClient

from tests.entities import user_example_1


async def test_create_user(async_client: AsyncClient):
    user = user_example_1
    response = await async_client.post("/api/users", data=user.json())
    assert response.status_code == 201
    assert "id" in response.json()


async def test_get_all_users(async_client: AsyncClient):
    response = await async_client.get("/api/users/all_users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0
    assert "id" in users[0]
    assert "first_name" in users[0]


async def test_get_user_profile(async_client: AsyncClient, created_user_id: str):
    response = await async_client.get(f"/api/users/{created_user_id}")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == created_user_id
    assert "first_name" in user
    assert "last_name" in user


async def test_get_user_profile_not_found(async_client: AsyncClient):
    user_id = str(uuid4())  # Simulate a non-existent user
    response = await async_client.get(f"/api/users/{user_id}")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == f"User with id='{user_id}' does not exist"


async def test_update_user(async_client: AsyncClient, created_user_id: str):
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
    response = await async_client.put(f"/api/users/{created_user_id}", data=update_data)
    assert response.status_code == 200
    user_ = await async_client.get(f"/api/users/{created_user_id}")
    user = user_.json()
    assert user["first_name"] == "John"
    assert user["last_name"] == "Smith"
    assert user["phone"] == 9876543210


async def test_update_user_no_data_provided(async_client: AsyncClient, created_user_id: str):
    response = await async_client.put(f"/api/users/{created_user_id}", data={})
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "No update data provided"


async def test_delete_user(async_client: AsyncClient, created_user_id: str):
    response = await async_client.delete(f"/api/users/{created_user_id}")
    assert response.status_code == 204


async def test_delete_user_not_found(async_client: AsyncClient):
    user_id = str(uuid4())  # Simulate a non-existent user
    response = await async_client.delete(f"/api/users/{user_id}")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == f"User with id='{user_id}' does not exist"
