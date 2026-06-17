from datetime import date
from pydantic import BaseModel, ConfigDict

from app.models import FilmGenre, FilmClassification


class FilmRead(BaseModel):
    id: int
    title: str
    director: str
    actors: str | None = None
    genre: FilmGenre
    min_duration: int
    classification: FilmClassification
    release_date: date | None = None
    language: str | None = None
    poster_url: str | None = None
    
    model_config = ConfigDict(from_attributes=True)

class FilmCreate(BaseModel):
    title: str
    director: str
    actors: str | None = None
    genre: FilmGenre
    min_duration: int
    classification: FilmClassification
    release_date: date | None = None
    language: str | None = None
    poster_url: str | None = None
    id_distributor: int
    
class FilmUpdate(BaseModel):
    title: str | None = None
    director: str | None = None
    actors: str | None = None
    genre: FilmGenre | None = None
    min_duration: int | None = None
    classification: FilmClassification | None = None
    release_date: date | None = None
    language: str | None = None
    poster_url: str | None = None
    id_distributor: int | None = None