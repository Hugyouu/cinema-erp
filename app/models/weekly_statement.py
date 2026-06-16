import enum
from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import Date, DateTime, Enum, ForeignKey, Identity, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .distribution_contract import DistributionContract
    from .invoice import Invoice


class StatementStatus(str, enum.Enum):
    DRAFT = "draft"
    VALIDATED = "validated"
    INVOICED = "invoiced"
    PAID = "paid"


class WeeklyStatement(Base):
    """Représente un relevé hebdomadaire de recettes pour un contrat de distribution."""

    __tablename__ = "weekly_statements"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("distribution_contracts.id"), nullable=False)
    week_start: Mapped[Date] = mapped_column(Date, nullable=False)
    week_end: Mapped[Date] = mapped_column(Date, nullable=False)
    gross_revenue: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    royalty_rate: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    royalty_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    status: Mapped[StatementStatus] = mapped_column(Enum(StatementStatus, name="statement_status"), nullable=True)
    generated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    contract: Mapped["DistributionContract"] = relationship(back_populates="weekly_statements")
    invoice: Mapped["Invoice"] = relationship(back_populates="statement")

    def __repr__(self) -> str:
        return f"WeeklyStatement(id={self.id}, contract_id={self.contract_id}, status={self.status})"
