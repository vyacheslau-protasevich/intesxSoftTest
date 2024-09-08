import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Base


class User(Base):

    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, index=True, default=uuid.uuid4
    )
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone: Mapped[int]
    address: Mapped[str]
    city: Mapped[str]
    state: Mapped[str]
    zipcode: Mapped[int]
    available: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    profile_photo: Mapped["ProfilePhoto"] = relationship()

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} id={self.id}>"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
