from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .film import Film
    from .distribution_contract import DistributionContract
    from .invoice import Invoice


class Distributor(Base):
    """Représente un distributeur de films."""

    __tablename__ = "distributors"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=True)

    films: Mapped[list["Film"]] = relationship(back_populates="distributor")
    contracts: Mapped[list["DistributionContract"]] = relationship(back_populates="distributor")
    invoices: Mapped[list["Invoice"]] = relationship(back_populates="distributor")

    def __repr__(self) -> str:
        return f"Distributor(id={self.id}, name={self.name!r}, country={self.country!r})"
