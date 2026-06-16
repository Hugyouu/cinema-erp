import enum
from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import Date, ForeignKey, Identity, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from .distributor import Distributor
    from .seance import Seance
    from .distribution_contract import DistributionContract

class FilmGenre(str, enum.Enum):
    ACTION = "action"
    AVENTURE = "aventure"
    COMEDIE = "comedie"
    DRAME = "drame"
    HORREUR = "horreur"
    SCIENCE_FICTION = "science_fiction"
    THRILLER = "thriller"
    ANIMATION = "animation"
    DOCUMENTAIRE = "documentaire"
    ROMANCE = "romance"
    FANTASTIQUE = "fantastique"
    POLICIER = "policier"
    HISTORIQUE = "historique"
    MUSICAL = "musical"


class FilmClassification(str, enum.Enum):
    TOUS_PUBLICS = "tous_publics"
    MOINS_10 = "-10"
    MOINS_12 = "-12"
    MOINS_16 = "-16"
    MOINS_18 = "-18"


class Film(Base):
    """Représente un film du catalogue, lié à un distributeur."""

    __tablename__ = "films"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    director: Mapped[str] = mapped_column(String(100), nullable=False)
    actors: Mapped[str] = mapped_column(String(255), nullable=True)
    min_duration: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[FilmGenre] = mapped_column(
        Enum(FilmGenre, name="film_genre"), nullable=False
    )
    classification: Mapped[FilmClassification] = mapped_column(
        Enum(FilmClassification, name="film_classification"),
        nullable=False,
    )
    release_date: Mapped[Date] = mapped_column(Date, nullable=True)
    language: Mapped[str] = mapped_column(String(50), nullable=True)
    poster_url: Mapped[str] = mapped_column(String(500), nullable=True)
    id_distributor: Mapped[int] = mapped_column(
        ForeignKey("distributors.id"), nullable=False
    )

    distributor: Mapped["Distributor"] = relationship(back_populates="films")
    seances: Mapped[list["Seance"]] = relationship(back_populates="film")
    contracts: Mapped[list["DistributionContract"]] = relationship(back_populates="film")

    def __repr__(self) -> str:
        return f"Film(id={self.id}, title={self.title!r}, genre={self.genre})"