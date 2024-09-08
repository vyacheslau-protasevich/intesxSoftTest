import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.models import Base


class ProfilePhoto(Base):

    __tablename__ = "profile_photos"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, index=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    photo_url: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<ProfilePhoto {self.id} user_id={self.user_id}>"

    def __str__(self):
        return f"{self.id} user_id={self.user_id}"
