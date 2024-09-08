from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from api.dependencies.stubs import get_sessionmaker
from db.repositories import UserRepository, ProfilePhotoRepository
from services.db.user import UserService


async def get_user_service(
    sessionmaker: async_sessionmaker[AsyncSession] = Depends(get_sessionmaker),
):
    async with sessionmaker() as session:
        yield UserService(
            session=session,
            user_repository=UserRepository(session),
            profile_photo_repository=ProfilePhotoRepository(session),
        )
