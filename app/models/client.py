from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import Date, DateTime, Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .subscription import Subscription
    from .reservation import Reservation


class Client(Base):
    """Représente un client inscrit sur la plateforme."""

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="client")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="client")

    def __repr__(self) -> str:
        return f"Client(id={self.id}, email={self.email!r})"
