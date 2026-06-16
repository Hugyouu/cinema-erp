import enum
from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import DateTime, Enum, ForeignKey, Identity, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .client import Client
    from .seance import Seance
    from .ticket import Ticket


class ResStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    USED = "used"


class Reservation(Base):
    """Représente une réservation faite par un client pour une séance."""

    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    seance_id: Mapped[int] = mapped_column(ForeignKey("seances.id"), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"), nullable=True)
    booking_ref: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[ResStatus] = mapped_column(Enum(ResStatus, name="res_status"), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    booked_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    seance: Mapped["Seance"] = relationship(back_populates="reservations")
    client: Mapped["Client"] = relationship(back_populates="reservations")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="reservation")

    def __repr__(self) -> str:
        return f"Reservation(id={self.id}, booking_ref={self.booking_ref!r}, status={self.status})"
