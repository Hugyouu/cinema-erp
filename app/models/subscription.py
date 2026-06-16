import enum
from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import Date, DateTime, Enum, ForeignKey, Identity, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .client import Client


class SubPlan(str, enum.Enum):
    MENSUEL = "mensuel"
    ANNUEL = "annuel"
    ILLIMITE = "illimite"


class SubStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class Subscription(Base):
    """Représente un abonnement souscrit par un client."""

    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    plan: Mapped[SubPlan] = mapped_column(Enum(SubPlan, name="sub_plan"), nullable=False)
    price_monthly: Mapped[int] = mapped_column(Integer, nullable=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=True)
    end_date: Mapped[Date] = mapped_column(Date, nullable=True)
    status: Mapped[SubStatus] = mapped_column(Enum(SubStatus, name="sub_status"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    client: Mapped["Client"] = relationship(back_populates="subscriptions")

    def __repr__(self) -> str:
        return f"Subscription(id={self.id}, client_id={self.client_id}, plan={self.plan}, status={self.status})"
