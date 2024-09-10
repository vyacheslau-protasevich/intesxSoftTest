from uuid import uuid4

from httpx import AsyncClient
from neo4j import Driver

from tests.entities import user_example_1, user_example_2, user_example_3


async def test_make_friends(async_client: AsyncClient, neo4j_driver: Driver):
    user_1 = user_example_1
    user_2 = user_example_2
    response = await async_client.post("/api/users", data=user_1.json())
    new_user_id_1 = response.json()["id"]
    response = await async_client.post("/api/users", data=user_2.json())
    new_user_id_2 = response.json()["id"]
    response = await async_client.post(f"/api/friends/friend_{new_user_id_1}_with_{new_user_id_2}")
    assert response.status_code == 201
    with neo4j_driver.session() as session:
        friends = session.run("MATCH (:User {id: $id})-[:FRIEND]-(:User {id: $id2}) RETURN COUNT(*) AS count",
                              id=new_user_id_2, id2=new_user_id_1)
        count = friends.single()["count"]
    assert count == 2


async def test_make_friends_already_friends(async_client: AsyncClient, neo4j_driver: Driver):
    with neo4j_driver.session() as session:
        result = session.run(
            """
                MATCH (u1:User)-[:FRIEND]-(u2:User)
                WHERE ID(u1) < ID(u2)
                RETURN u1, u2
                LIMIT 1
            """
        )
        friends = result.data()
        friend_1 = friends[0]["u1"]["id"]
        friend_2 = friends[0]["u2"]["id"]
        response = await async_client.post(f"/api/friends/friend_{friend_1}_with_{friend_2}")
        assert response.status_code == 400
        assert response.json()["detail"] == f"Users with id='{friend_1}' and id='{friend_2}' are already friends"


async def test_make_friends_not_found(async_client: AsyncClient):
    user_id_1 = str(uuid4())
    user_id_2 = str(uuid4())
    response = await async_client.post(f"/api/friends/friend_{user_id_1}_with_{user_id_2}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"User with id='{user_id_1}' does not exist"


async def test_make_friends_with_self(async_client: AsyncClient, created_user_id: str):
    response = await async_client.post(f"/api/friends/friend_{created_user_id}_with_{created_user_id}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot make friends with self"


async def test_get_friends(async_client: AsyncClient):
    user_1 = user_example_1
    user_2 = user_example_2
    response = await async_client.post("/api/users", data=user_1.json())
    new_user_id_1 = response.json()["id"]
    response = await async_client.post("/api/users", data=user_2.json())
    new_user_id_2 = response.json()["id"]
    await async_client.post(f"/api/friends/friend_{new_user_id_1}_with_{new_user_id_2}")
    response = await async_client.get(f"/api/friends/all_friends_of_{new_user_id_1}")
    assert response.status_code == 200
    friends = response.json()
    assert isinstance(friends, list)
    assert len(friends) == 1


async def test_get_friends_not_found(async_client: AsyncClient):
    user_id = str(uuid4())
    response = await async_client.get(f"/api/friends/all_friends_of_{user_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"User with id='{user_id}' does not exist"


async def test_get_shortest_path(async_client: AsyncClient, neo4j_driver: Driver):
    user_1 = user_example_1
    user_2 = user_example_2
    user_3 = user_example_3
    response = await async_client.post("/api/users", data=user_1.json())
    new_user_id_1 = response.json()["id"]
    response = await async_client.post("/api/users", data=user_2.json())
    new_user_id_2 = response.json()["id"]
    response = await async_client.post("/api/users", data=user_3.json())
    new_user_id_3 = response.json()["id"]
    await async_client.post(f"/api/friends/friend_{new_user_id_1}_with_{new_user_id_2}")
    await async_client.post(f"/api/friends/friend_{new_user_id_2}_with_{new_user_id_3}")
    response = await async_client.get(f"/api/friends/shortest_path_from_{new_user_id_1}_to_{new_user_id_3}")
    assert response.status_code == 200
    path = response.json()
    assert isinstance(path, list)
    assert len(path) == 1


async def test_get_shortest_path_not_found(async_client: AsyncClient):
    user_id_1 = str(uuid4())
    user_id_2 = str(uuid4())
    response = await async_client.get(f"/api/friends/shortest_path_from_{user_id_1}_to_{user_id_2}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"User with id='{user_id_1}' does not exist"


async def test_get_shortest_path_no_path_found(async_client: AsyncClient, neo4j_driver: Driver):
    user_1 = user_example_1
    user_2 = user_example_2
    response = await async_client.post("/api/users", data=user_1.json())
    new_user_id_1 = response.json()["id"]
    response = await async_client.post("/api/users", data=user_2.json())
    new_user_id_2 = response.json()["id"]
    response = await async_client.get(f"/api/friends/shortest_path_from_{new_user_id_1}_to_{new_user_id_2}")
    assert response.status_code == 404
    assert response.json()[
               "detail"] == f"No path found between users with id='{new_user_id_1}' and id='{new_user_id_2}'"
