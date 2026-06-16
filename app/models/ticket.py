from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import Boolean, ForeignKey, Identity, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .reservation import Reservation


class Ticket(Base):
    """Représente un ticket individuel lié à une réservation."""

    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id"), nullable=False)
    ticket_type: Mapped[str] = mapped_column(String(50), nullable=True)
    seat_number: Mapped[str] = mapped_column(String(20), nullable=True)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    is_used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    reservation: Mapped["Reservation"] = relationship(back_populates="tickets")

    def __repr__(self) -> str:
        return f"Ticket(id={self.id}, seat_number={self.seat_number!r}, is_used={self.is_used})"
