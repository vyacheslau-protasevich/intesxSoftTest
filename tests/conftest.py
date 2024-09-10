import asyncio
import datetime
import uuid
from testcontainers.compose import DockerCompose

from httpx import AsyncClient
import pytest

from src.config import Settings
from src.main import app

from neo4j import GraphDatabase, Driver


@pytest.fixture(scope="session")
async def created_user_id(neo4j_driver: Driver) -> str:
    with neo4j_driver.session() as session:
        result = session.run("MATCH (u:User) RETURN u.id LIMIT 1")
        a = result.single()["u.id"]
        return str(a)


@pytest.fixture(autouse=True, scope="session")
def config() -> Settings:
    return Settings()


@pytest.fixture(autouse=True, scope="session")
async def neo4j_driver(config: Settings):
    driver = GraphDatabase.driver(config.neo4j_uri, auth=(config.neo4j_user, config.neo4j_password))
    yield driver
    driver.close()


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
