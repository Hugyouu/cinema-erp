from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import ForeignKey, Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .film import Film
    from .distributor import Distributor
    from .royalty_tier import RoyaltyTier
    from .weekly_statement import WeeklyStatement


class DistributionContract(Base):
    """Représente un contrat de distribution entre un film et un distributeur."""

    __tablename__ = "distribution_contracts"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    film_id: Mapped[int] = mapped_column(ForeignKey("films.id"), nullable=False)
    distributor_id: Mapped[int] = mapped_column(ForeignKey("distributors.id"), nullable=False)
    start_at: Mapped[str] = mapped_column(String(50), nullable=True)
    end_at: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=True)

    film: Mapped["Film"] = relationship(back_populates="contracts")
    distributor: Mapped["Distributor"] = relationship(back_populates="contracts")
    royalty_tiers: Mapped[list["RoyaltyTier"]] = relationship(back_populates="contract")
    weekly_statements: Mapped[list["WeeklyStatement"]] = relationship(back_populates="contract")

    def __repr__(self) -> str:
        return f"DistributionContract(id={self.id}, film_id={self.film_id}, distributor_id={self.distributor_id})"
