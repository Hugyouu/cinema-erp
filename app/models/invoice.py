import enum
from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import Date, Enum, ForeignKey, Identity, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .distributor import Distributor
    from .weekly_statement import WeeklyStatement


class InvoiceStatus(str, enum.Enum):
    ISSUED = "issued"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Invoice(Base):
    """Représente une facture émise vers un distributeur pour un relevé hebdomadaire."""

    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    distributor_id: Mapped[int] = mapped_column(ForeignKey("distributors.id"), nullable=False)
    statement_id: Mapped[int] = mapped_column(ForeignKey("weekly_statements.id"), nullable=False)
    amount_ht: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    amount_ttc: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    issued_at: Mapped[Date] = mapped_column(Date, nullable=True)
    due_date: Mapped[Date] = mapped_column(Date, nullable=True)
    status: Mapped[InvoiceStatus] = mapped_column(Enum(InvoiceStatus, name="invoice_status"), nullable=False)

    distributor: Mapped["Distributor"] = relationship(back_populates="invoices")
    statement: Mapped["WeeklyStatement"] = relationship(back_populates="invoice")

    def __repr__(self) -> str:
        return f"Invoice(id={self.id}, invoice_number={self.invoice_number!r}, status={self.status})"
