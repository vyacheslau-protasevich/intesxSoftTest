from httpx import AsyncClient
from neo4j import Driver


async def test_create_random_user_and_friends(async_client: AsyncClient, neo4j_driver: Driver):
    with neo4j_driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    response = await async_client.post("/api/random/random_5_users_3_friends")
    assert response.status_code == 200
    with neo4j_driver.session() as session:
        friends = session.run("MATCH ()-[r:FRIEND]-() RETURN COUNT(r) AS numberOfFriends")
        friends_count = friends.single()["numberOfFriends"]
        users = session.run("MATCH (u:User) RETURN COUNT(u) AS numberOfUsers")
        users_count = users.single()["numberOfUsers"]
    assert users_count == 5
    assert friends_count == 3 * 4


async def test_create_random_user_and_friends_error(async_client: AsyncClient, neo4j_driver: Driver):
    response = await async_client.post("/api/random/random_5_users_25_friends")
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot make friends with such amount of users"