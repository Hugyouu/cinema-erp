import enum
from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import Identity, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .seance import Seance


class RoomType(str, enum.Enum):
    STANDARD = "standard"
    THREE_D = "3D"
    IMAX = "IMAX"
    FOUR_DX = "4DX"


class Room(Base):
    """Représente une salle de cinéma."""

    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[RoomType] = mapped_column(
        Enum(RoomType, name="room_type"), nullable=False
    )

    seances: Mapped[list["Seance"]] = relationship(back_populates="room")

    def __repr__(self) -> str:
        return f"Room(id={self.id}, name={self.name!r}, type={self.type}, capacity={self.capacity})"
