from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    phone: int
    address: str
    city: str
    state: str = Field(min_length=2, max_length=2)
    zipcode: int
    available: bool


class UserOut(BaseUser):
    id: UUID
    created_at: datetime
    profile_photo_url: str | None = None


class UserIn(BaseUser):
    profile_photo_url: str | None = None


class UserCreate(BaseUser):
    ...


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: int | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zipcode: int | None = None
    available: bool | None = None


class UserUpdateIn(UserUpdate):
    profile_photo: str | None = None
