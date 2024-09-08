from uuid import UUID

from sqlalchemy import insert, select, delete, update

from db.repositories.base import BaseDbRepository
from db.models import ProfilePhoto


class ProfilePhotoRepository(BaseDbRepository):

    async def create_photo(self, photo_url: str, user_id: UUID) -> ProfilePhoto:
        return await self.session.scalar(
            insert(ProfilePhoto)
            .values(photo_url=photo_url, user_id=user_id)
            .returning(ProfilePhoto)
        )

    async def get_user_photo(self, user_id: UUID) -> ProfilePhoto | None:
        return await self.session.scalar(
            select(ProfilePhoto)
            .where(ProfilePhoto.user_id == user_id)
        )

    async def delete_photo_by_user_id(self, user_id: UUID) -> UUID | None:
        return await self.session.scalar(
            delete(ProfilePhoto)
            .where(ProfilePhoto.user_id == user_id)
            .returning(ProfilePhoto.photo_url)
        )

    async def update_photo_by_user_id(self, user_id: UUID, photo_url: str) -> None:
        await self.session.execute(
            update(ProfilePhoto)
            .values(photo_url=photo_url)
            .where(ProfilePhoto.user_id == user_id)
        )
