from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Film
from app.schemas.film import FilmCreate, FilmRead, FilmUpdate

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("/", response_model=list[FilmRead])
def get_films(db: Session = Depends(get_db)):
    return db.query(Film).all()


@router.get("/{film_id}", response_model=FilmRead)
def get_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film


@router.post("/", response_model=FilmRead, status_code=201)
def create_film(film: FilmCreate, db: Session = Depends(get_db)):
    new_film = Film(**film.model_dump())
    db.add(new_film)
    db.commit()
    db.refresh(new_film)
    return new_film


@router.patch("/{film_id}", response_model=FilmRead)
def update_film(film_id: int, film: FilmUpdate, db: Session = Depends(get_db)):
    existing = db.query(Film).filter(Film.id == film_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Film not found")
    for field, value in film.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{film_id}", status_code=204)
def delete_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    db.delete(film)
    db.commit()
