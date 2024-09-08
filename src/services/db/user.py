from uuid import UUID

from fastapi.exceptions import HTTPException
from starlette import status

from exceptions.user import UserDoesNotExistError
from models.user import UserCreate, UserOut, UserUpdate, UserIn, UserUpdateIn
from db.repositories import UserRepository, ProfilePhotoRepository

from sqlalchemy.ext.asyncio import AsyncSession


class UserService:

    def __init__(
            self,
            session: AsyncSession,
            user_repository: UserRepository,
            profile_photo_repository: ProfilePhotoRepository
    ) -> None:
        self.session = session
        self.user_repository = user_repository
        self.profile_photo_repository = profile_photo_repository

    async def get_user_by_id(self, user_id: UUID) -> UserOut:
        user = await self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise UserDoesNotExistError(str(user_id))
        if user.profile_photo.photo_url:
            profile_photo_url = user.profile_photo.photo_url
        else:
            profile_photo_url = None
        return UserOut(**user.__dict__, profile_photo_url=profile_photo_url)

    async def get_users_list(self) -> list[UserOut]:
        users = await self.user_repository.get_users_list()
        return [UserOut(**user.__dict__, profile_photo_url=user.profile_photo.photo_url) for user in users]

    async def create_user(self, user: UserIn) -> UserOut:
        user_to_create = UserCreate(**user.__dict__)
        created_user = await self.user_repository.create_user(user_to_create)
        if user.profile_photo_url:
            await self.profile_photo_repository.create_photo(photo_url=user.profile_photo_url, user_id=created_user.id)
        await self.session.commit()
        return UserOut(**created_user.__dict__)

    async def update_user(self, user_id: UUID, user_data: UserUpdateIn) -> None:
        data_to_update = UserUpdate(**user_data.model_dump())
        if data_to_update.model_dump(exclude_none=True):
            await self.user_repository.update_user(user_id, data_to_update)
        if user_data.profile_photo:
            await self.profile_photo_repository.update_photo_by_user_id(user_id, user_data.profile_photo)
        await self.session.commit()

    async def delete_user(self, user_id: UUID) -> None:
        await self.user_repository.delete_user(user_id)
        await self.profile_photo_repository.delete_photo_by_user_id(user_id)
        await self.session.commit()

    async def get_current_user(self, user_id: UUID) -> UserOut:
        try:
            user = await self.get_user_by_id(user_id)
        except UserDoesNotExistError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist"
            )
        return user

