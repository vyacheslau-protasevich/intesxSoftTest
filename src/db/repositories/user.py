from uuid import UUID

from sqlalchemy import select, insert, update, delete

from sqlalchemy.orm import joinedload

from db.repositories.base import BaseDbRepository
from db.models import User
from models.user import UserCreate, UserUpdate


class UserRepository(BaseDbRepository):

    async def get_users_list(self) -> list[User]:
        users = await self.session.execute(
            select(User)
            .options(joinedload(User.profile_photo))
            .order_by(User.last_name, User.first_name)
        )
        return list(users.scalars().all())

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.session.scalar(
            select(User)
            .options(joinedload(User.profile_photo))
            .where(User.id == user_id)
        )

    async def create_user(self, user: UserCreate) -> User:
        return await self.session.scalar(
            insert(User)
            .values(**user.model_dump())
            .returning(User)
        )

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> None:
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                **user_data.model_dump(exclude_unset=True, exclude_none=True)
            )
        )

    async def delete_user(self, user_id: UUID) -> None:
        await self.session.execute(
            delete(User)
            .where(User.id == user_id)
        )
