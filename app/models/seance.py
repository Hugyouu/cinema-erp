import enum
from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import ForeignKey, Identity, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .film import Film
    from .room import Room
    from .reservation import Reservation


class SeanceFormat(str, enum.Enum):
    VF = "VF"
    VO = "VO"
    VOSTFR = "VOSTFR"


class SeanceStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    OPEN = "open"
    CLOSED = "closed"
    FULL = "full"
    CANCELLED = "cancelled"


class Seance(Base):
    """Représente une séance, liée à un film et une salle."""

    __tablename__ = "seances"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    film_id: Mapped[int] = mapped_column(ForeignKey("films.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    start_at: Mapped[str] = mapped_column(String(50), nullable=True)
    end_at: Mapped[str] = mapped_column(String(50), nullable=True)
    format: Mapped[SeanceFormat] = mapped_column(
        Enum(SeanceFormat, name="seance_format"), nullable=True
    )
    status: Mapped[SeanceStatus] = mapped_column(
        Enum(SeanceStatus, name="seance_status"), nullable=True
    )
    seats_sold: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    film: Mapped["Film"] = relationship(back_populates="seances")
    room: Mapped["Room"] = relationship(back_populates="seances")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="seance")

    def __repr__(self) -> str:
        return f"Seance(id={self.id}, film_id={self.film_id}, start_at={self.start_at!r}, status={self.status})"
