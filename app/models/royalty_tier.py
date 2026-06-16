from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import ForeignKey, Identity, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .distribution_contract import DistributionContract


class RoyaltyTier(Base):
    """Représente un palier de royalties pour une semaine donnée d'un contrat."""

    __tablename__ = "royalty_tiers"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("distribution_contracts.id"), nullable=False)
    week_number: Mapped[int] = mapped_column(Integer, nullable=True)
    percentage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)

    contract: Mapped["DistributionContract"] = relationship(back_populates="royalty_tiers")

    def __repr__(self) -> str:
        return f"RoyaltyTier(id={self.id}, contract_id={self.contract_id}, week_number={self.week_number}, percentage={self.percentage})"
