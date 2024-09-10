import asyncio
import datetime
import uuid

from httpx import AsyncClient
import pytest
from neo4j import GraphDatabase

from src.config import Settings
from src.main import app


@pytest.fixture(scope="session")
async def created_book_id(session_maker: async_sessionmaker[AsyncSession]) -> str:
    async with session_maker() as session:
        result = await session.execute(text("SELECT books.book_id from books LIMIT 1;"))
    return str(result.scalar_one())


@pytest.fixture(scope="session")
async def test_admin_user() -> AdminUserExample:
    return AdminUserExample(
        user_id=uuid.UUID("53bf51fa-08c3-4ace-be33-347f4504cc9c"),
        name="Test user name",
        device_id="13371488xxx",
        email="test.user@gmail.com",
        password="1",
        hashed_password="$2b$12$ao91w17KXBX6gj6P3mkwI.dFTBTYzF4jjUgnLJt/alfaP.vGjWFqC",
        completed_tutorial=True,
        preferred_genres=["haha", "hehe", "hoho"],
        role=UserRole.ADMIN,
        gender=UserGender.MALE,
        language="en",
        registered_at=datetime.datetime(year=2024, month=1, day=1)
    )

@pytest.fixture(autouse=True, scope="session")
def config() -> Settings:
    return Settings()

@pytest.fixture(scope="session")
async def session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )