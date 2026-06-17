from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Seance
from app.schemas.seance import SeanceCreate, SeanceRead, SeanceUpdate

router = APIRouter(prefix="/seances", tags=["Séances"])


@router.get("/", response_model=list[SeanceRead])
def get_seances(db: Session = Depends(get_db)):
    return db.query(Seance).all()


@router.get("/{seance_id}", response_model=SeanceRead)
def get_seance(seance_id: int, db: Session = Depends(get_db)):
    seance = db.query(Seance).filter(Seance.id == seance_id).first()
    if not seance:
        raise HTTPException(status_code=404, detail="Séance not found")
    return seance


@router.post("/", response_model=SeanceRead, status_code=201)
def create_seance(seance: SeanceCreate, db: Session = Depends(get_db)):
    new_seance = Seance(**seance.model_dump())
    db.add(new_seance)
    db.commit()
    db.refresh(new_seance)
    return new_seance


@router.patch("/{seance_id}", response_model=SeanceRead)
def update_seance(seance_id: int, seance: SeanceUpdate, db: Session = Depends(get_db)):
    existing = db.query(Seance).filter(Seance.id == seance_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Séance not found")
    for field, value in seance.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{seance_id}", status_code=204)
def delete_seance(seance_id: int, db: Session = Depends(get_db)):
    seance = db.query(Seance).filter(Seance.id == seance_id).first()
    if not seance:
        raise HTTPException(status_code=404, detail="Séance not found")
    db.delete(seance)
    db.commit()
