from httpx import AsyncClient


async def test_get_my_profile(
    async_client: AsyncClient,
    admin_jwt_token: str,
    test_admin_user: AdminUserExample
):
    response = await async_client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {admin_jwt_token}"}
    )
    assert response.status_code == 200
    content = response.json()
    assert content["role"] == test_admin_user.role.value
    assert content["email"] == test_admin_user.email
    assert content["gender"] == test_admin_user.gender.value
    assert content["language"] == test_admin_user.language
    assert content["completed_tutorial"] == test_admin_user.completed_tutorial
    assert content["preferred_genres"] == test_admin_user.preferred_genres